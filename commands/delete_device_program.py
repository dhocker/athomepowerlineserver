#
# Delete a device program
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.program_assignments import ProgramAssignments
from timers.TimerStore import TimerStore


class DeleteDeviceProgram(ServerCommand.ServerCommand):
    """
    Command handler for deleting a device timer program
    """
    def Execute(self, request):
        args = request["args"]
        device_id = int(args["device-id"])
        program_id = int(args["program-id"])

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        try:
            # Remove program from database and in-memory cache
            result = ProgramAssignments.delete(device_id, program_id)

            if result:
                r['result-code'] = 0
                r['device-id'] = args["device-id"]
                r['program-id'] = args["program-id"]
                r['message'] = "Success"
            else:
                # Probably invalid device type
                r['result-code'] = 1
                r['device-id'] = args["device-id"]
                r['program-id'] = args["program-id"]
                r['error'] = 1
                r['message'] = "Failure"
        except Exception as ex:
            r['result-code'] = 1
            r['device-id'] = args["device-id"]
            r['program-id'] = args["program-id"]
            r['error'] = 2
            r['message'] = str(ex)

        return r
