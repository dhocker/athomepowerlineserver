#
# Query for all defined programs
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
import json


class QueryPrograms(ServerCommand):
    """
    Command handler for querying for all programs
    """
    def Execute(self, request):
        args = request["args"]
        pd = Programs()
        if "program-id" in args.keys():
            result = pd.get_program_by_id(int(args["program-id"]))
            key = "program"
        else:
            result = pd.get_all_programs()
            key = "programs"

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result or len(result) >= 0:
            r['result-code'] = ServerCommand.SUCCESS
            r[key] = result
            r['message'] = ServerCommand.MSG_SUCCESS
        else:
            # Probably invalid device type
            r['result-code'] = pd.last_error_code
            r['message'] = pd.last_error

        return r
