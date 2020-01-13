#
# Assign a program to a device
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.program_assignments import ProgramAssignments


class AssignProgram(ServerCommand.ServerCommand):
    """
    Command handler for assigning a program to a device
    """
    def Execute(self, request):
        device_id = request["args"]["device-id"]
        program_id = request["args"]["program-id"]

        result = ProgramAssignments.insert(device_id, program_id)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result >= 0:
            r['result-code'] = 0
            r['program-assignment-id'] = result
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
