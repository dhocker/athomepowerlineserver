#
# Turn off all devices
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
from database.managed_devices import ManagedDevices


class AllDevicesOff(ServerCommand.ServerCommand):
    """
    Command handler for turning on all selected devices
    """
    def Execute(self, request):
        # All defined devices
        devices = ManagedDevices.get_all_devices()

        device_count = 0
        for device in devices:
            device_count += 1
            driver = self.get_driver_for_id(device["id"])
            result = driver.device_off(device["mfg"], device["name"], device["address"], device["channel"])
            if result:
                device_count -= 1

        # Generate a successful response
        r = self.CreateResponse(request["request"])

        if device_count == 0:
            r['result-code'] = 0
            r['message'] = "Success"
        else:
            # One or more devices did not turn off
            r['result-code'] = 1
            r['error'] = 1
            r['message'] = "{0} devices failed to turn off".format(device_count)

        return r
