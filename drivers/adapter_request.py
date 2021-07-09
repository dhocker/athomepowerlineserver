#
# Request for the thread based adapter for meross-iot async module
# Copyright © 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import threading


class AdapterRequest:
    """
    Basically a container for passing a request to the adapter thread
    """
    # Requests
    OPEN = "open"
    CLOSE = "close"
    DEVICE_ON = "deviceon"
    DEVICE_OFF = "deviceoff"
    SET_COLOR = "setcolor"
    SET_BRIGHTNESS = "setbrightness"
    GET_AVAILABLE_DEVICES = "getavailabledevices"
    DISCOVER_DEVICES = "discoverdevices"
    GET_DEVICE_TYPE = "getdevicetype"
    ON_OFF_STATUS = "onoffstatus"

    def __init__(self, request=None, kwargs=None):
        """
        Create a request instance
        :param request:
        :param kwargs:
        """
        self.request = request
        self.kwargs = kwargs if kwargs is not None else {}
        self._complete_event = threading.Event()
        self.result = None

        # Last error for this request
        self._last_error_code = 0
        self._last_error = None

    @property
    def last_error_code(self):
        return self._last_error_code

    @last_error_code.setter
    def last_error_code(self, v):
        self._last_error_code = v

    @property
    def last_error(self):
        return self._last_error

    @last_error.setter
    def last_error(self, v):
        self._last_error = v

    def wait(self, timeout=60.0):
        """
        Wait for the request to complete
        :param timeout: In seconds, the maximum wait time
        :return:
        """
        return self._complete_event.wait(timeout=float(timeout))

    def is_complete(self):
        """
        Answers the question: Is the request complete?
        :return: True is the request is complete
        """
        return self._complete_event.is_set()

    def set_complete(self, result):
        """
        Post the completion event
        :param result: The result to be posted
        :return: None
        """
        self.result = result
        self._complete_event.set()
