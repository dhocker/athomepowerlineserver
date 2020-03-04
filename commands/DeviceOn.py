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

import commands.ServerCommand as ServerCommand


#######################################################################
# Command handler for on command
class DeviceOn(ServerCommand.ServerCommand):

    #######################################################################
    # Execute the "on" command.
    def Execute(self, request):
        device_id = int(request["args"]["device-id"])

        driver = self.get_driver_for_id(device_id)
        device = self.get_device_for_id(device_id)
        driver.set_brightness(device["mfg"], device["name"], device["address"], device["channel"], device["brightness"])
        driver.set_color(device["mfg"], device["name"], device["address"], device["channel"], device["color"])
        r = self.CreateResponse(request["request"])
        try:
            result = driver.device_on(device["mfg"], device["name"], device["address"], device["channel"])
            if result:
                r['result-code'] = ServerCommand.ServerCommand.SUCCESS
                r['message'] = ServerCommand.ServerCommand.MSG_SUCCESS
            else:
                r['result-code'] = ServerCommand.ServerCommand.SERVER_ERROR
                r['device-code'] = driver.last_error_code
                r['message'] = driver.last_error
        except Exception as ex:
            r['result-code'] = ServerCommand.ServerCommand.SERVER_ERROR
            r['message'] = str(ex)

        return r
