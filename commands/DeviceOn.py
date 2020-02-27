#
# Device on
# Copyright © 2014, 2019  Dave Hocker
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
        driver.set_color(device["mfg"], device["name"], device["address"], device["channel"], device["color"])
        result = driver.DeviceOn(device["mfg"], device["name"], device["address"], device["channel"])

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        r['result-code'] = driver.LastErrorCode
        if result:
            # r['error'] = "Command not fully implemented"
            r['message'] = "Success"
        else:
            r['error'] = driver.LastError
            r['message'] = driver.LastError

        return r
