#
# Query for all defined devices
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


class QueryPrograms(ServerCommand.ServerCommand):
    """
    Command handler for querying for all programs
    """
    def Execute(self, request):
        args = request["args"]
        if "program-id" in args.keys():
            result = Programs.get_program_by_id(int(args["program-id"]))
            key = "program"
        else:
            result = Programs.GetAll()
            key = "programs"

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result or len(result) >= 0:
            r['result-code'] = 0
            r[key] = result
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r