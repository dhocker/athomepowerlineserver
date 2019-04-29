#
# Define a new device
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


class DefineDevice(ServerCommand.ServerCommand):
    """
    Command handler for defining a new device
    """
    def Execute(self, request):
        device_name = request["args"]["device-name"]
        device_type = request["args"]["device-type"]
        device_address = request["args"]["device-address"]

        # TODO Consider a unique check on the name
        # TODO Cases based on type for address validation?

        result = Devices.insert(device_name, device_type, device_address)

        # Generate a successful response
        response = self.CreateResponse(request["request"])
        r = response["X10Response"]

        if result >= 0:
            r['result-code'] = 0
            r['device-id'] = result
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return response
