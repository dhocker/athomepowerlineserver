#
# Query for all available programs to a device
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.programs import Programs


class QueryAvailablePrograms(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        deviceid = int(request["args"]["device-id"])
        result = Programs.get_all_available_programs(deviceid)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            r['result-code'] = 0
            r['programs'] = result
            r['message'] = "Success"
        else:
            # No records found
            r['result-code'] = 0
            r['programs'] = []
            r['message'] = "No records found"

        return r
