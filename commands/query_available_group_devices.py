#
# Query for all available devices to a group
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from database.managed_devices import ManagedDevices


class QueryAvailableGroupDevices(ServerCommand):
    """
    Command handler for querying for all available group devices
    """
    def Execute(self, request):
        groupid = int(request["args"]["group-id"])
        md = ManagedDevices()
        result = md.get_all_available_group_devices(groupid)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result is not None:
            r['result-code'] = ServerCommand.SUCCESS
            r['devices'] = result
            r['message'] = ServerCommand.MSG_SUCCESS
        else:
            r['result-code'] = md.last_error_code
            r['devices'] = []
            r['message'] = md.last_error

        return r
