#
# AtHomeAPI - networked server for X10 and WiFi devices
# Copyright © 2019, 2020 Dave Hocker (email: AtHomeX10@gmail.com)
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

        while True:
            c = sock.recv(1).decode()
            json_data += c

            if c == "{":
                depth += 1
            if c == "}":
                depth -= 1
                if depth == 0:
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

    # Device related methods

    def device_on(self, device_id, color=None, brightness=None):
        """
        Send device on command to a device that is registered in the AHPS database
        :param device_id:
        :param color:
        :param brightness:
        :return:
        """
        data = self._create_request("On")
        data["args"]["device-id"] = device_id

        # Optional color and brightness overrides
        if color is not None:
            data["args"]["device-color"] = color
        if brightness is not None:
            data["args"]["device-brightness"] = brightness

        return self._send_command(data)

    def device_off(self, device_id):
        """
        Send device off command to a device that is registered in the AHPS database
        :param device_id:
        :return:
        """
        data = self._create_request("Off")
        data["args"]["device-id"] = device_id

        return self._send_command(data)

    def new_device_on(self, device_mfg, device_address, device_channel,
                      device_color, device_brightness, device_name=None):
        """
        Turn a new device on ( a new device is not in the AHPS database)
        :param device_mfg:
        :param device_address:
        :param device_channel:
        :param device_name:
        :param device_color:
        :param device_brightness:
        :return:
        """
        data = self._create_request("On")
        data["args"]["device-mfg"] = device_mfg
        data["args"]["device-address"] = device_address
        data["args"]["device-channel"] = device_channel
        data["args"]["device-color"] = device_color
        data["args"]["device-brightness"] = device_brightness
        if device_name is not None:
            data["args"]["device-name"] = device_name

        return self._send_command(data)

    def new_device_off(self, device_mfg, device_address, device_channel, device_name=None):
        data = self._create_request("Off")
        data["args"]["device-mfg"] = device_mfg
        data["args"]["device-address"] = device_address
        data["args"]["device-channel"] = device_channel
        if device_name is not None:
            data["args"]["device-name"] = device_name

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

    def all_devices_off(self):
        """
        Send all units off command
        :return:
        """
        data = self._create_request("AllDevicesOff")

        return self._send_command(data)

    def all_devices_on(self):
        """
        Send all lights on command
        :return:
        """
        data = self._create_request("AllDevicesOn")

        return self._send_command(data)

    def query_devices(self):
        """
        Query for all devices
        :return:
        """
        req = self._create_request("QueryDevices")
        response = self._send_command(req)
        return response

    def query_all_available_devices(self, manufacturer):
        """
        Query for all available devices of a given type
        :return:
        """
        req = self._create_request("QueryAvailableDevices")
        req["args"]["type"] = manufacturer
        response = self._send_command(req)
        return response

    def query_device(self, device_id):
        """
        Query a device by its device id
        :param device_id:
        :return:
        """
        req = self._create_request("QueryDevices")
        req["args"]["device-id"] = device_id
        response = self._send_command(req)
        return response

    def define_device(self, device_name, device_location, device_mfg,
                      device_address, device_channel, device_color, device_brightness):
        """
        Define (create) a new device
        :param device_name:
        :param device_location:
        :param device_mfg:
        :param device_address:
        :param device_channel
        :param device_color:
        :param device_brightness
        :return:
        """
        req = self._create_request("DefineDevice")
        req["args"]["device-name"] = device_name
        req["args"]["device-location"] = device_location
        req["args"]["device-mfg"] = device_mfg
        req["args"]["device-address"] = device_address
        req["args"]["device-channel"] = device_channel
        req["args"]["device-color"] = device_color
        req["args"]["device-brightness"] = device_brightness
        response = self._send_command(req)
        return response

    def update_device(self, device_id, device_name, device_location, device_mfg, device_address,
                      device_channel, device_color, device_brightness):
        """
        Update an existing device
        :param device_id:
        :param device_name:
        :param device_location:
        :param device_mfg:
        :param device_address:
        :param device_channel:
        :param device_color:
        :param device_brightness:
        :return:
        """
        req = self._create_request("UpdateDevice")
        req["args"]["device-id"] = device_id
        req["args"]["device-name"] = device_name
        req["args"]["device-location"] = device_location
        req["args"]["device-mfg"] = device_mfg
        req["args"]["device-address"] = device_address
        req["args"]["device-channel"] = device_channel
        req["args"]["device-color"] = device_color
        req["args"]["device-brightness"] = device_brightness

        response = self._send_command(req)
        return response

    def delete_device(self, device_id):
        """
        Delete a device by its device id
        :param device_id:
        :return:
        """
        req = self._create_request("DeleteDevice")
        req["args"]["device-id"] = device_id
        response = self._send_command(req)
        return response

    # Program related methods

    def delete_program(self, program_id):
        """
        Delete a program by its ID
        :param program_id:
        :return:
        """
        req = self._create_request("DeleteProgram")
        req["args"]["program-id"] = program_id
        response = self._send_command(req)
        return response

    def get_programs_for_device_id(self, device_id):
        """
        Query for all programs for a given device id
        :param device_id:
        :return:
        """
        req = self._create_request("QueryDevicePrograms")
        req["args"]["device-id"] = device_id
        response = self._send_command(req)
        return response

    def get_available_programs_for_device_id(self, device_id):
        """
        Query for all programs available for assignment to a given device id
        :param device_id:
        :return:
        """
        req = self._create_request("QueryAvailablePrograms")
        req["args"]["device-id"] = device_id
        response = self._send_command(req)
        return response

    def assign_program_to_device(self, device_id, program_id):
        req = self._create_request("AssignProgram")
        req["args"]["device-id"] = device_id
        req["args"]["program-id"] = program_id
        response = self._send_command(req)
        return response

    def assign_program_to_group_devices(self, group_id, program_id):
        req = self._create_request("AssignProgramToGroup")
        req["args"]["group-id"] = group_id
        req["args"]["program-id"] = program_id
        response = self._send_command(req)
        return response

    def get_program_by_id(self, program_id):
        """
        Query for a program by its id
        :param program_id:
        :return:
        """
        req = self._create_request("QueryDeviceProgram")
        req["args"]["program-id"] = program_id
        response = self._send_command(req)
        return response

    def define_device_program(self, program):
        req = self._create_request("DefineProgram")
        req["args"] = program
        response = self._send_command(req)
        return response

    def update_device_program(self, program):
        req = self._create_request("UpdateProgram")
        req["args"] = program
        response = self._send_command(req)
        return response

    def delete_device_program(self, device_id, program_id):
        """
        Delete a device program from its device
        :param device_id:
        :param program_id:
        :return:
        """
        req = self._create_request("DeleteDeviceProgram")
        req["args"]["device-id"] = device_id
        req["args"]["program-id"] = program_id
        response = self._send_command(req)
        return response

    # Action group methods

    def get_all_action_groups(self):
        """
        Query for all action groups
        :return:
        """
        req = self._create_request("QueryActionGroups")
        response = self._send_command(req)
        return response

    def get_action_group(self, group_id):
        """
        Query for an action group
        :return:
        """
        req = self._create_request("QueryActionGroup")
        req["args"]["group-id"] = group_id
        response = self._send_command(req)
        return response

    def define_action_group(self, group_name):
        """
        Define (create) a new device
        :param group_name:
        :return:
        """
        req = self._create_request("DefineActionGroup")
        req["args"]["group-name"] = group_name
        response = self._send_command(req)
        return response

    def delete_action_group(self, group_id):
        """
        Delete a device group
        :param group_id:
        :return:
        """
        req = self._create_request("DeleteActionGroup")
        req["args"]["group-id"] = group_id
        response = self._send_command(req)
        return response

    def update_action_group(self, group):
        req = self._create_request("UpdateActionGroup")
        req["args"] = group
        response = self._send_command(req)
        return response

    def get_action_group_devices(self, group_id):
        """
        Query for all devices in an action group
        :return:
        """
        req = self._create_request("QueryActionGroupDevices")
        req["args"]["group-id"] = group_id
        response = self._send_command(req)
        return response

    def get_available_devices_for_group_id(self, group_id):
        """
        Query for all devices available for assignment to a given group id
        :param group_id:
        :return:
        """
        req = self._create_request("QueryAvailableGroupDevices")
        req["args"]["group-id"] = group_id
        response = self._send_command(req)
        return response

    def assign_device_to_group(self, group_id, device_id):
        req = self._create_request("AssignDevice")
        req["args"]["group-id"] = group_id
        req["args"]["device-id"] = device_id
        response = self._send_command(req)
        return response

    def group_on(self, group_id):
        """
        Send group on command
        :param group_id:
        :return:
        """
        data = self._create_request("GroupOn")
        data["args"]["group-id"] = group_id

        return self._send_command(data)

    def group_off(self, group_id):
        """
        Send group off command
        :param group_id:
        :return:
        """
        data = self._create_request("GroupOff")
        data["args"]["group-id"] = group_id

        return self._send_command(data)

    def delete_action_group_device(self, group_id, device_id):
        """
        Send delete device from action group
        :param group_id:
        :param device_id
        :return:
        """
        data = self._create_request("DeleteActionGroupDevice")
        data["args"]["group-id"] = group_id
        data["args"]["device-id"] = device_id

        return self._send_command(data)
