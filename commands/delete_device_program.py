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
from database.programs import Programs
from timers.TimerStore import TimerStore


class DeleteDeviceProgram(ServerCommand.ServerCommand):
    """
    Command handler for deleting a device timer program
    """
    def Execute(self, request):
        args = request["args"]
        # Remove program from database and in-memory cache
        result = Programs.delete(int(args["program-id"]))
        TimerStore.remove_timer(int(args["program-id"]))

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            r['result-code'] = 0
            r['program-id'] = args["program-id"]
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['program-id'] = args["program-id"]
            r['error'] = 1
            r['message'] = "Failure"

        return r
