#
# Query for all devices in an action group
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from database.action_group_devices import ActionGroupDevices


class QueryActionGroupDevices(ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]

        agd = ActionGroupDevices()
        result = agd.get_group_devices(int(args["group-id"]))

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result or len(result) >= 0:
            r['result-code'] = 0
            r["devices"] = result
            r['message'] = "Success"
        else:
            # Probably bad group ID
            r['result-code'] = agd.last_error_code
            r['message'] = agd.last_error

        return r
