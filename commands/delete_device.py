#
# Delete a device
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.managed_devices import ManagedDevices
from timers.TimerStore import TimerStore


class DeleteDevice(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]
        result = ManagedDevices.delete_device(int(args["device-id"]))

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            r['result-code'] = 0
            r['device-id'] = args["device-id"]
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
