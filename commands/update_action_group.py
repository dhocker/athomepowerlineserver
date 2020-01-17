#
# Update an existing action group
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


class UpdateActionGroup(ServerCommand.ServerCommand):
    """
    Command handler for updating an existing device
    """
    def Execute(self, request):
        group_id = request["args"]["group-id"]
        group_name = request["args"]["group-name"]

        result = ActionGroups.update(group_id, group_name)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            r['result-code'] = 0
            r['group-id'] = group_id
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
