#
# Assign a device to a group
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


class AssignDevice(ServerCommand):
    """
    Command handler for assigning a device to a group
    """
    def Execute(self, request):
        device_id = request["args"]["device-id"]
        group_id = request["args"]["group-id"]

        agd = ActionGroupDevices()
        result = agd.insert_device(group_id, device_id)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result >= 0:
            r['result-code'] = AssignDevice.SUCCESS
            r['action-group-device-id'] = result
            r['message'] = AssignDevice.MSG_SUCCESS
        else:
            # Probably invalid device type
            r['result-code'] = agd.last_error
            r['message'] = agd.last_error_code

        return r
