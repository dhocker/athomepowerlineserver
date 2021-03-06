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

import socketserver
import json
import logging
import CommandHandler

logger = logging.getLogger("server")


class MyTCPHandlerJson(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    call_sequence = 1

    """
    This handler uses raw data from the SocketServer.TCPServer class.
    """

    def handle(self):
        logger.info("Request from %s", self.client_address[0])
        # self.request is the TCP socket connected to the client
        self.raw_json = self.ReadJson()
        # logger.info("raw json: %s", self.raw_json)
        # logger.info("Request length: %s", len(self.raw_json))

        try:
            self.json = json.loads(self.raw_json)
            logger.info("Request: %s", self.json["request"])
            # logger.info("Args: %s", json.dumps(self.json["args"]))

            # The command handler generates the response
            response = CommandHandler.CommandHandler().Execute(self.json)

            logger.info("Request completed")
        except Exception as ex:
            logger.error("Exception occurred while parsing json request")
            logger.error(str(ex))
            logger.error(self.raw_json)
            # Send an error response
            response = CommandHandler.CommandHandler.CreateErrorResponse(self.json["request"],
                                                                         CommandHandler.CommandHandler.UnhandledException,
                                                                         "Unhandled exception occurred", ex.message)
        finally:
            pass

        # Return the response to the client
        self.request.sendall(json.JSONEncoder().encode(response).encode())

        MyTCPHandlerJson.call_sequence += 1

    def ReadJson(self):
        """
        Read a JSON payload from a socket
        """
        depth = 0
        json_data = ""

        while (True):
            c = self.request.recv(1).decode()

            if (len(json_data) == 0) and (c == "\""):
                pass
            else:
                json_data += c

            if (c == "{"):
                depth += 1
            elif (c == "}"):
                depth -= 1
                if (depth == 0):
                    return json_data
