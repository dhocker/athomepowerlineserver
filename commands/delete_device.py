#
# Delete a device
# Copyright © 2019, 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.managed_devices import ManagedDevices


class DeleteDevice(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]
        md = ManagedDevices()
        result = md.delete_device(int(args["device-id"]))

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result >= 0:
            r['result-code'] = ServerCommand.ServerCommand.SUCCESS
            r['device-id'] = args["device-id"]
            r['message'] = ServerCommand.ServerCommand.MSG_SUCCESS
        else:
            # Probably invalid device type
            r['result-code'] = md.last_error_code
            r['message'] = md.last_error

        return r
