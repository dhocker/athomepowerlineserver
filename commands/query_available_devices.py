#
# Query for all available devices of a given type
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from drivers.device_driver_manager import DeviceDriverManager

class QueryAvailableDevices(ServerCommand.ServerCommand):
    """
    Command handler for querying for all available devices
    """
    def Execute(self, request):
        args = request["args"]
        result = {}
        if "type" in args.keys():
            driver = DeviceDriverManager.get_driver(args['type'])
            result = driver.GetAvailableDevices()

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result or len(result) >= 0:
            r['result-code'] = 0
            r['devices'] = result
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
