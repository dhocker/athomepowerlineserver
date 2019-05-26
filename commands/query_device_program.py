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

import commands.ServerCommand as ServerCommand
from database.Timers import Timers


class QueryDeviceProgram(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        programid = int(request["args"]["program-id"])
        result = Timers.get_device_program(programid)

        # Generate a successful response
        response = self.CreateResponse(request["request"])
        r = response["X10Response"]

        if result:
            r['result-code'] = 0
            r['program'] = result
            r['message'] = "Success"
        else:
            # No records found
            r['result-code'] = 0
            r['programs'] = []
            r['message'] = "No records found"

        return response
