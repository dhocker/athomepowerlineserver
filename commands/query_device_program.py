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
from database.programs import Programs
import json


class QueryDeviceProgram(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        programid = int(request["args"]["program-id"])
        result = Programs.get_program_by_id(programid)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            # The args column is a string. Turn it into a dict.
            r['result-code'] = 0
            r['program'] = result
            r['message'] = "Success"
        else:
            # No records found
            r['result-code'] = 0
            r['programs'] = []
            r['message'] = "No records found"

        return r
