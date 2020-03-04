#
# Query for all defined devices
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


class QueryDevices(ServerCommand.ServerCommand):
    """
    Command handler for querying for all devices
    """
    def Execute(self, request):
        args = request["args"]

        md = ManagedDevices()
        if "device-id" in args.keys():
            device_id = request["args"]["device-id"]
            result = md.get_device(int(device_id))
            if result:
                # Add device specific properties to result (from driver)
                driver = self.get_driver_for_id(device_id)
                result["type"] = driver.get_device_type(result["address"], result["channel"])
            key = "device"
        else:
            result = md.get_all_devices()
            if result:
                # Add device specific properties to each result (from driver)
                for device in result:
                    driver = self.get_driver_for_id(device["id"])
                    device["type"] = driver.get_device_type(device["address"], device["channel"])
            key = "devices"

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if result or len(result) >= 0:
            r['result-code'] = ServerCommand.ServerCommand.SUCCESS
            r[key] = result
            r['message'] = ServerCommand.ServerCommand.MSG_SUCCESS
        else:
            # Probably invalid device type
            r['result-code'] = md.last_error_code
            r['message'] = md.last_error

        return r
