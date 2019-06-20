#
# AtHomePowerlineServer - networked server for X10 and WiFi devices
# Copyright © 2019 Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# API module for the AtHomeServer
#

import socket
import json


class ServerRequest:
    def __init__(self, host="localhost", port=9999, verbose=True):
        """
        Create an instance of a server request
        :param host:
        :param port:
        :param verbose:
        """
        self.host = host
        self.port = port
        self.verbose = verbose

    @classmethod
    def _create_request(cls, command):
        """
        Create a template of a request
        :return:
        """
        request = {}
        request["request"] = command
        # The args parameter is an dictionary.
        request["args"] = {}
        return request

    def _connect_to_server(self):
        """
        Open a socket to the server
        Note that a socket can only be used for one request.
        The server seems to close the socket at when it is
        finished handling the request.
        :return:
        """
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and check status
            sock.connect((self.host, self.port))
            return sock
        except Exception as ex:
            print("Unable to connect to server:", self.host, self.port)
            print(str(ex))

        return None

    @classmethod
    def _read_json(cls, sock):
        """
        Read a JSON payload from a socket
        :return:
        """
        depth = 0
        json_data = ""

        while (True):
            c = sock.recv(1).decode()
            json_data += c

            if (c == "{"):
                depth += 1
            if (c == "}"):
                depth -= 1
                if (depth == 0):
                    return json_data

    def _display_response(self, response):
        """
        Display a formatted response on the console
        :return:
        """
        jr = json.loads(response)
        print("Response for request:", jr["request"])
        if self.verbose:
            print(json.dumps(jr, indent=2))
        else:
            print("  result-code:", jr["result-code"])
            print("  message:", jr["message"])

    def _send_command(self, data):
        """
        Send a command to the server
        :param data: A dict containing the request definition.
        It will be serialized to a JSON payload.
        :return: Returns the response as a dict.
        """
        # Convert the payload structure into json text.
        # Effectively this serializes the payload.
        json_data = json.JSONEncoder().encode(data).encode()

        # Create a socket connection to the server
        sock = self._connect_to_server()
        if sock is None:
            return None

        # send status request to server
        try:
            print("Sending request:", data["request"])
            if self.verbose:
                print(json.dumps(data, indent=2))
            sock.sendall(json_data)

            # Receive data from the server and shut down
            json_data = self._read_json(sock)

            # print "Sent:     {}".format(data)
            # print "Received: {}".format(json_data)
            self._display_response(json_data)
        except Exception as ex:
            print(str(ex))
            json_data = None
        finally:
            sock.close()

        return json.loads(json_data)

    def status_request(self):
        request = self._create_request("StatusRequest")
        return self._send_command(request)

    def open_request(self, request):
        """
        An open server request. The argument is a dict
        containing the entire request. This is a "raw"
        interface to the server.
        :param request: request
        :return:
        """
        result = self._send_command(request)
        return result

    def device_on(self, device_id, dimamount):
        """

        :param device_id:
        :param dimamount:
        :return:
        """
        data = self._create_request("On")
        data["args"]["device-id"] = device_id
        data["args"]["dim-amount"] = dimamount

        return self._send_command(data)

    def device_off(self, device_id, dimamount):
        """

        :param device_id:
        :param dimamount:
        :return:
        """
        data = self._create_request("Off")
        data["args"]["device-id"] = device_id
        data["args"]["dim-amount"] = dimamount

        return self._send_command(data)

    def device_dim(self, device_id, dimamount):
        """

        :param device_id:
        :param dimamount:
        :return:
        """
        data = self._create_request("Dim")
        data["args"]["device-id"] = device_id
        data["args"]["dim-amount"] = dimamount

        return self._send_command(data)

    def device_bright(self, device_id, brightamount):
        """

        :param device_id:
        :param brightamount:
        :return:
        """
        data = self._create_request("Bright")
        data["args"]["device-id"] = device_id
        data["args"]["bright-amount"] = brightamount

        return self._send_command(data)

    def define_program(self, program):
        data = self._create_request("DefineProgram")
        data["args"] = program

        return self._send_command(data)

    def update_program(self, program):
        data = self._create_request("UpdateProgram")
        data["args"] = program

        return self._send_command(data)

    def delete_program(self, program_id):
        data = self._create_request("DeleteDeviceProgram")
        data["args"]["program-id"] = program_id

        return self._send_command(data)

    def define_device(self, device):
        data = self._create_request("DefineDevice")
        data["args"] = device

        return self._send_command(data)

    def update_device(self, device):
        data = self._create_request("UpdateDevice")
        data["args"] = device

        return self._send_command(data)

    def delete_device(self, device_id):
        data = self._create_request("DeleteDevice")
        data["args"]["device-id"] = device_id

        return self._send_command(data)

    def query_device(self, device_id):
        data = self._create_request("QueryDevices")
        data["args"]["device-id"] = device_id
        return self._send_command(data)

    def query_devices(self):
        data = self._create_request("QueryDevices")
        return self._send_command(data)

    def query_device_programs(self, device_id):
        data = self._create_request("QueryDevicePrograms")
        data["args"]["device-id"] = device_id
        return self._send_command(data)

    def query_device_program(self, program_id):
        data = self._create_request("QueryDeviceProgram")
        data["args"]["program-id"] = program_id
        return self._send_command(data)
