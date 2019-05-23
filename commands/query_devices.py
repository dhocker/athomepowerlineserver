#
# Query for all devices
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.devices import Devices


class QueryDevices(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]
        if "device-id" in args.keys():
            result = Devices.get_device(int(args["device-id"]))
            key = "device"
        else:
            result = Devices.get_all_devices()
            key = "devices"

        # Generate a successful response
        response = self.CreateResponse(request["request"])
        r = response["X10Response"]

        if result:
            r['result-code'] = 0
            r[key] = result
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return response
