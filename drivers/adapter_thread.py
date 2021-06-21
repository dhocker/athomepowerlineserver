#
# Thread based adapter for modules that use asyncio
# Copyright © 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# Reference: https://github.com/albertogeniola/MerossIot
# See also meross_asyncio_test.py
#
# The Meross-iot module makes significant use of asyncio. asyncio has a
# number of limitations that make it somewhat difficult to deal with in
# a multi-threaded application.
# The asyncio documentation itself explicitly states that it is not
# inherently thread safe. It appears to have been designed to run
# on the main thread.
#
# The athomeserver uses multiple threads.
# For example, each network connection (read incoming command) arrives on its
# own thread. The timer program thread checks and triggers timer programs.
# Device drivers are initialized on the main thread.
#
# This means that all Meross-iot code must be isolated to a single thread.
# Otherwise, asyncio will throw thread related exceptions when least expected.
#
# This adapter is inherently thread safe. The request queue (a Queue) is used as the
# synchronization method. A Queue is thread safe (see Queue.put and Queue.get).
# The adapter takes/gets one request at a time from the request queue making it
# thread safe.
#

import threading
import queue
import asyncio
import logging
import datetime
from .adapter_request import AdapterRequest

logger = logging.getLogger("server")


class AdapterThread(threading.Thread):
    # Error codes
    UNDEFINED = -1
    SUCCESS = 0
    MEROSS_ERROR = 7
    RETRY_COUNT = 5

    def __init__(self, name="AdapterThread"):
        super().__init__(name=name)
        self._request = None
        self._loop = None

        # For terminating the adapter thread
        self._terminate_event = threading.Event()
        # For sending requests to the thread
        self._request_queue = queue.Queue()

    @property
    def last_error_code(self):
        return self._request.last_error_code

    @last_error_code.setter
    def last_error_code(self, v):
        self._request.last_error_code = v

    @property
    def last_error(self):
        return self._request.last_error

    @last_error.setter
    def last_error(self, v):
        self._request.last_error = v

    def clear_last_error(self):
        """
        Reset the last error info
        :return: None
        """
        self.last_error_code = AdapterThread.UNDEFINED
        self.last_error = None

    def run(self):
        """
        Run the realtime request server.
        This method is called on the new thread by the Thread class.
        The server terminates when the close request is received.
        :return:
        """

        # This loop can only be used by this thread
        self._loop = asyncio.new_event_loop()

        # Note that the close method sets the terminate event
        while not self._terminate_event.is_set():
            # This is a blocking call. The adapter thread will wait here
            # until a request arrives.
            # Termination occurs when the close() method is called and the terminate event is set.
            self._request = self._request_queue.get()
            start_time = datetime.datetime.now()

            # Cases for each request/command
            result = self.dispatch_request()

            self._request.set_complete(result)
            elapsed_time = datetime.datetime.now() - start_time
            logger.debug("%s elapsed time: %f", self._request.request, elapsed_time.total_seconds())

            # We are finished with this request
            self._request = None

        # Thread clean up
        self._loop.stop()
        self._loop.close()
        self._loop = None

    def dispatch_request(self):
        """
        Dispatch a request to the device module. Must be implemented in a derived class.
        :return:
        """
        raise NotImplementedError

    def queue_request(self, request):
        """
        Queue a request for execution on the Meross adapter thread.
        If the adapter thread is waiting for a request, it will automatically
        start running.
        :param request:
        :return:
        """
        self._request_queue.put(request)
