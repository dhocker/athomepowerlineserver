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

    @property
    def LastErrorCode(self):
        return self._last_error_code

    @LastErrorCode.setter
    def LastErrorCode(self, v):
        self._last_error_code = v

    @property
    def LastError(self):
        return self._last_error

    @LastError.setter
    def LastError(self, v):
        self._last_error = v

    def Open(self):
        pass

    def Close(self):
        pass

    def DeviceOn(self, device_type, device_name_tag, house_device_code, dim_amount):
        pass

    def DeviceOff(self, device_type, device_name_tag, house_device_code, dim_amount):
        pass

    def DeviceDim(self, device_type, device_name_tag, house_device_code, dim_amount):
        pass

    def DeviceBright(self, device_type, device_name_tag, house_device_code, bright_amount):
        pass

    def DeviceAllUnitsOff(self, house_code):
        pass

    def DeviceAllLightsOff(self, house_code):
        pass

    def DeviceAllLightsOn(self, house_code):
        pass

    def GetAvailableDevices(self):
        """
        Get all known available devices of a given type. Not every device can be discovered.
        For example TPLink/Kasa devices can be discovered, but X10 devices
        cannot be discovered.
        :return: Returns a dict where the key is the major device identifier or address
        and the value is the human readable name of the device.
        """
        return {}

    # TODO Consider defining this as SetCurrentTime taking no parameters.
    # Set the controller time to the current, local time.
    def SetTime(self, time_value):
        raise NotImplementedError()

    # Reset the last error info
    def ClearLastError(self):
        self.LastErrorCode = 0
        self.LastError = None
