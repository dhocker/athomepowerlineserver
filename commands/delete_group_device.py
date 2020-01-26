#
# Delete a device from a group
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


class DeleteActionGroupDevice(ServerCommand):
    """
    Command handler for assigning a device to a group
    """
    def Execute(self, request):
        device_id = request["args"]["device-id"]
        group_id = request["args"]["group-id"]

        result = ActionGroupDevices.delete_device(group_id, device_id)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        # The result is the number of devices deleted
        if result >= 0:
            r['result-code'] = 0
            r['group-id'] = group_id
            r['device_id'] = device_id
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
