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

from commands.ServerCommand import ServerCommand
from database.programs import Programs


class DeleteProgram(ServerCommand):
    """
    Command handler for deleting a program and its associated uses
    """
    def Execute(self, request):
        args = request["args"]

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        try:
            pd = Programs()
            result = pd.delete(int(args["program-id"]))

            r['result-code'] = pd.last_error_code
            r['device-id'] = args["program-id"]
            r['message'] = pd.last_error
        except Exception as ex:
            # A likely cause of an Exception would be a cascading delete error
            r['result-code'] = DeleteProgram.SERVER_ERROR
            r['program-id'] = args["program-id"]
            r['message'] = str(ex)

        return r
