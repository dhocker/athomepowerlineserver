#
# Delete a device group
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from database.action_groups import ActionGroups


class DeleteGroup(ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]
        result = ActionGroups.delete(int(args["group-id"]))

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            r['result-code'] = 0
            r['group-id'] = args["group-id"]
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
