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
        result = ManagedDevices.get_all_available_group_devices(groupid)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            r['result-code'] = 0
            r['devices'] = result
            r['message'] = "Success"
        else:
            # No records found
            r['result-code'] = 0
            r['programs'] = []
            r['message'] = "No records found"

        return r
