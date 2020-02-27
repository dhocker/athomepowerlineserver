# -*- coding: utf-8 -*-
#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright © 2014, 2015  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Device off
#

import commands.ServerCommand as ServerCommand


#######################################################################
# Command handler for off command
class DeviceOff(ServerCommand.ServerCommand):

    #######################################################################
    # Execute the "of" command.
    def Execute(self, request):
        device_id = int(request["args"]["device-id"])

        driver = self.get_driver_for_id(device_id)
        device = self.get_device_for_id(device_id)
        result = driver.device_off(device["mfg"], device["name"], device["address"], device["channel"])

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        r['result-code'] = driver.last_error_code
        if result:
            # r['error'] = "Command not fully implemented"
            r['message'] = "Success"
        else:
            r['error'] = driver.last_error
            r['message'] = driver.last_error

        return r
