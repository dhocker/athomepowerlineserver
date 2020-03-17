#
# Device on
# Copyright © 2014, 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand


#######################################################################
# Command handler for on command
class DeviceOn(ServerCommand):

    #######################################################################
    # Execute the "on" command.
    def Execute(self, request):
        """
        Two cases: (1) device ID present or (2) device info present and no device ID
        :param request:
        :return:
        """
        if "device-id" in request["args"].keys():
            device_id = int(request["args"]["device-id"])

            driver = self.get_driver_for_id(device_id)
            device = self.get_device_for_id(device_id)

            device_mfg = device["mfg"]
            device_name = device["name"]
            device_address = device["address"]
            device_channel = int(device["channel"])
            device_color = device["color"]
            device_brightness = device["brightness"]
        elif "device-mfg" in request["args"].keys() and \
                "device-address" in request["args"].keys() and \
                "device-channel" in request["args"].keys():
            # If there is no device ID, there must be mfg, address and channel
            device_mfg = request["args"]["device-mfg"]
            device_address = request["args"]["device-address"]
            device_channel = int(request["args"]["device-channel"])
            device_color = ""
            device_brightness = 100
            # Name is optional
            device_name = request["args"]["device-name"] if "device-name" in request["args"].keys() else ""

            # Driver for mfg/type
            driver = self.get_driver_for_mfg(device_mfg)
        else:
            r = self.CreateResponse(request["request"])
            r['result-code'] = ServerCommand.BAD_REQUEST
            r['message'] = "Either device ID or mfg+address+channel is required"
            return r

        # Look for color and brightness overrides. These are optional.
        if "device-color" in request["args"].keys():
            device_color = request["args"]["device-color"]
        if "device-brightness" in request["args"].keys():
            device_brightness = request["args"]["device-brightness"]

        r = self.CreateResponse(request["request"])
        try:
            driver.set_brightness(device_mfg, device_name, device_address, device_channel, device_brightness)
            driver.set_color(device_mfg, device_name, device_address, device_channel, device_color)
            result = driver.device_on(device_mfg, device_name, device_address, device_channel)
            if result:
                r['result-code'] = ServerCommand.SUCCESS
                r['message'] = ServerCommand.MSG_SUCCESS
            else:
                r['result-code'] = driver.last_error_code
                r['message'] = driver.last_error
        except Exception as ex:
            r['result-code'] = ServerCommand.SERVER_ERROR
            r['message'] = str(ex)

        return r
