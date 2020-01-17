#
# Define a new action group
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.action_groups import ActionGroups


class DefineGroup(ServerCommand.ServerCommand):
    """
    Command handler for defining a new device
    """
    def Execute(self, request):
        group_name = request["args"]["group-name"]

        result = ActionGroups.insert(group_name)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result >= 0:
            r['result-code'] = 0
            r['group-id'] = result
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
