#
# Delete a device program
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from database.program_assignments import ProgramAssignments


class DeleteDeviceProgram(ServerCommand):
    """
    Command handler for deleting a device timer program
    """
    def Execute(self, request):
        args = request["args"]
        device_id = int(args["device-id"])
        program_id = int(args["program-id"])

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        # Remove program from database
        pa = ProgramAssignments()
        result = pa.delete(device_id, program_id)

        if result:
            r['result-code'] = DeleteDeviceProgram.SUCCESS
            r['device-id'] = args["device-id"]
            r['program-id'] = args["program-id"]
            r['message'] = DeleteDeviceProgram.MSG_SUCCESS
        else:
            r['result-code'] = pa.last_error_code
            r['device-id'] = args["device-id"]
            r['program-id'] = args["program-id"]
            r['message'] = pa.last_error

        return r
