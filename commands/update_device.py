#
# Update an existing device
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.managed_devices import ManagedDevices


class UpdateDevice(ServerCommand.ServerCommand):
    """
    Command handler for updating an existing device
    """
    def Execute(self, request):
        device_id = request["args"]["device-id"]
        device_name = request["args"]["device-name"]
        device_location = request["args"]["device-location"]
        device_mfg = request["args"]["device-mfg"]
        device_address = request["args"]["device-address"]
        device_channel = 0
        if "device-channel" in request["args"].keys():
            device_channel = int(request["args"]["device-channel"])

        # TODO Consider a unique check on the name
        # TODO Cases based on type for address validation?

        result = ManagedDevices.update(device_id, device_name, device_location, device_mfg,
                                       device_address, device_channel)

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result:
            r['result-code'] = 0
            r['device-id'] = device_id
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
