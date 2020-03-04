#
# Define a new device
# Copyright © 2019, 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.managed_devices import ManagedDevices


class DefineDevice(ServerCommand.ServerCommand):
    """
    Command handler for defining a new device
    """
    def Execute(self, request):
        device_name = request["args"]["device-name"]
        device_location = request["args"]["device-location"]
        device_mfg = request["args"]["device-mfg"]
        device_address = request["args"]["device-address"]
        device_channel = int(request["args"]["device-channel"])
        device_color = request["args"]["device-color"]
        device_brightness = int(request["args"]["device-brightness"])

        # TODO Consider a unique check on the name
        # TODO Cases based on type for address validation?

        md = ManagedDevices()
        result = md.insert(device_name, device_location, device_mfg,
                                       device_address, device_channel, device_color, device_brightness)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result >= 0:
            r['result-code'] = ServerCommand.ServerCommand.SUCCESS
            r['device-id'] = result
            r['message'] = ServerCommand.ServerCommand.MSG_SUCCESS
        else:
            # Probably invalid device type
            r['result-code'] = md.last_error_code
            r['message'] = md.last_error

        return r
