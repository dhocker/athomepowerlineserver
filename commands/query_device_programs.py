#
# Query for all timer programs for a device
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from database.programs import Programs


class QueryDevicePrograms(ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        deviceid = int(request["args"]["device-id"])
        pd = Programs()
        result = pd.get_all_device_programs(deviceid)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result is not None:
            r['result-code'] = ServerCommand.SUCCESS
            r['programs'] = result
            r['message'] = ServerCommand.MSG_SUCCESS
        else:
            # No records found
            r['result-code'] = pd.last_error_code
            r['programs'] = []
            r['message'] = pd.last_error

        return r
