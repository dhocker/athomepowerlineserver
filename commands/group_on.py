#
# Group on
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
# Command handler for group on command
class GroupOn(ServerCommand):

    #######################################################################
    # Execute the "on" command.
    def Execute(self, request):
        group_id = int(request["args"]["group-id"])

        r = self.CreateResponse(request["request"])

        agd = ActionGroupDevices()
        group_devices = agd.get_group_devices(group_id)
        if group_devices is None:
            r['result-code'] = agd.last_error_code
            r['message'] = agd.last_error
            return r
        on_count = 0
        for group_device in group_devices:
            driver = self.get_driver_for_id(group_device["id"])
            result = driver.device_on(group_device["mfg"], group_device["name"], group_device["address"], group_device["channel"])
            if request:
                on_count += 1
            else:
                # Trap the last error so it can be reported back to the client
                last_error = driver.last_error
                last_error_code = driver.last_error_code

        if on_count == len(group_devices):
            r['result-code'] = ServerCommand.SUCCESS
            r['message'] = ServerCommand.MSG_SUCCESS
        else:
            r['result-code'] = last_error_code
            r['message'] = last_error

        return r
