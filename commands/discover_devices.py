#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from drivers.device_driver_manager import DeviceDriverManager


# Command handler for discover devices request
class DiscoverDevices(ServerCommand):

    # Execute the status request command.
    # You might think we have to call the controller to get its
    # status, but it is not clear that is necessary.
    def Execute(self, request):
        # Discover devices for all supported manufacturers
        DeviceDriverManager.discover_devices()

        r = DiscoverDevices.CreateResponse("DiscoverDevices")
        r['result-code'] = 0
        r['message'] = "Success"

        return r