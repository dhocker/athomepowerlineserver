#
# Turn on all selected devices
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


class AllSelectedDevicesOn(ServerCommand.ServerCommand):
    """
    Command handler for turning on all selected devices
    """
    def Execute(self, request):
        # All defined devices
        devices = ManagedDevices.get_all_devices()

        device_count = 0
        for device in devices:
            # We're only interested in selected devices
            if device["selected"]:
                device_count += 1
                driver = self.get_driver_for_id(device["id"])
                result = driver.DeviceOn(device["type"], device["name"], device["address"], 0)
                if result:
                    device_count -= 1

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if device_count == 0:
            r['result-code'] = 0
            r['message'] = "Success"
        else:
            # One or more devices did not turn on
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "{0} devices failed to turn on".format(device_count)

        return r
