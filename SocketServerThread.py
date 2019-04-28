#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Socket server running on its own thread
#

import threading
import ThreadedTCPServer
import MyTCPHandlerJson
import logging

logger = logging.getLogger("server")


# This class should be used as a singleton
class SocketServerThread:
    # Constructor of an instance to server a given host:port
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_thread = threading.Thread(target=self.RunServer)
        ThreadedTCPServer.ThreadedTCPServer.allow_reuse_address = True
        self.server = ThreadedTCPServer.ThreadedTCPServer((host, port), MyTCPHandlerJson.MyTCPHandlerJson)

    # Start the TCPServer on its own thread
    def Start(self):
        self.server_thread.start()

    # Stop the TCPServer thread
    def Stop(self):
        logger.info("Shutting down TCPServer thread")
        self.server.shutdown()
        self.server_thread.join()
        logger.info("TCPServer thread down")

    # Run TCPServer on a new thread
    def RunServer(self):
        logger.info("Now serving sockets at %s:%s", self.host, self.port)
        self.server.serve_forever()
