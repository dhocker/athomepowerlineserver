#
# Query for all available programs to a device
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


class QueryAvailablePrograms(ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        deviceid = int(request["args"]["device-id"])
        pd = Programs()
        result = pd.get_all_available_programs(deviceid)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result is not None:
            r['result-code'] = QueryAvailablePrograms.SUCCESS
            r['programs'] = result
            r['message'] = QueryAvailablePrograms.MSG_SUCCESS
        else:
            # No records found
            r['result-code'] = pd.last_error_code
            r['programs'] = []
            r['message'] = pd.last_error

        return r
