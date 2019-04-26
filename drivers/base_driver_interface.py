#
# AtHomePowerlineServer - base class for a device driver
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Defines the interface contract for a device driver
#

import logging

logger = logging.getLogger("server")


class BaseDriverInterface:
    def __init__(self):
        self.ClearLastError()
        logger.info("Device driver base class initialized")

    def Open(self):
        pass

    def Close(self):
        pass

    def DeviceOn(self, house_device_code, dim_amount):
        pass

    def DeviceOff(self, house_device_code, dim_amount):
        pass

    def DeviceDim(self, house_device_code, dim_amount):
        pass

    def DeviceBright(self, house_device_code, dim_amount):
        pass

    def DeviceAllUnitsOff(self, house_code):
        pass

    def DeviceAllLightsOff(self, house_code):
        pass

    def DeviceAllLightsOn(self, house_code):
        pass

    # TODO Consider defining this as SetCurrentTime taking no parameters.
    # Set the controller time to the current, local time.
    def SetTime(self, time_value):
        raise NotImplementedError()

    # Reset the last error info
    def ClearLastError(self):
        self.LastErrorCode = 0
        self.LastError = None
