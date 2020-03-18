#
# Query for all action groups
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


class QueryActionGroups(ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]
        ag = ActionGroups()
        if "group-id" in args.keys():
            result = ag.get_group(int(args["group-id"]))
            key = "group"
        else:
            result = ag.get_all_groups()
            key = "groups"

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result or len(result) >= 0:
            r['result-code'] = ServerCommand.SUCCESS
            r[key] = result
            r['message'] = ServerCommand.MSG_SUCCESS
        else:
            r['result-code'] = ag.last_error_code
            r['message'] = ag.last_error

        return r
