#
# Delete a program
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


class DeleteProgram(ServerCommand.ServerCommand):
    """
    Command handler for deleting a program and its associated uses
    """
    def Execute(self, request):
        args = request["args"]

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        try:
            result = Programs.delete(int(args["program-id"]))

            if result:
                r['result-code'] = 0
                r['device-id'] = args["program-id"]
                r['message'] = "Success"
            else:
                # Probably invalid device type
                r['result-code'] = 1
                r['error'] = 1
                r['message'] = "Failure"
        except Exception as ex:
            # A likely cause of an Exception would be a cascading delete error
            r['result-code'] = 1
            r['program-id'] = args["program-id"]
            r['error'] = 2
            r['message'] = str(ex)

        return r
