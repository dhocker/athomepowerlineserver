# -*- coding: utf-8 -*-
#
# Group off
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from database.action_group_devices import ActionGroupDevices


#######################################################################
# Command handler for group off command
class GroupOff(ServerCommand):

    #######################################################################
    # Execute the "of" command.
    def Execute(self, request):
        group_id = int(request["args"]["group-id"])

        group_devices = ActionGroupDevices.get_group_devices(group_id)
        for group_device in group_devices:
            driver = self.get_driver_for_id(group_device["id"])
            result = driver.device_off(group_device["mfg"], group_device["name"], group_device["address"], group_device["channel"])

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
