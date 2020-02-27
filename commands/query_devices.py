#
# Query for all defined devices
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


class QueryDevices(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]
        if "device-id" in args.keys():
            device_id = request["args"]["device-id"]
            result = ManagedDevices.get_device(int(device_id))
            # Add device specific properties to result (from driver)
            driver = self.get_driver_for_id(device_id)
            result["type"] = driver.get_device_type(result["address"], result["channel"])
            key = "device"
        else:
            result = ManagedDevices.get_all_devices()
            # Add device specific properties to each result (from driver)
            for device in result:
                driver = self.get_driver_for_id(device["id"])
                device["type"] = driver.get_device_type(device["address"], device["channel"])
            key = "devices"

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result or len(result) >= 0:
            r['result-code'] = 0
            r[key] = result
            r['message'] = "Success"
        else:
            # Probably invalid device type
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "Failure"

        return r
