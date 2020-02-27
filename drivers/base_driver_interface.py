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
    # Device types
    DEVICE_TYPE_PLUG = "plug"
    DEVICE_TYPE_BULB = "bulb"
    DEVICE_TYPE_STRIP = "strip"

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

    def set_color(self, device_type, device_name_tag, house_device_code, channel, hex_color):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Device address or UUID
        :param channel: 0-n
        :param hex_color: Hex color #RRGGBB
        :return:
        """
        pass

    def set_brightness(self, device_type, device_name_tag, house_device_code, channel, brightness):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Device address or UUID
        :param channel: 0-n
        :param brightness: 0-100 percent
        :return:
        """
        pass

    def DeviceOn(self, device_type, device_name_tag, house_device_code, channel):
        pass

    def DeviceOff(self, device_type, device_name_tag, house_device_code, channel):
        pass

    def DeviceDim(self, device_type, device_name_tag, house_device_code, channel, dim_amount):
        pass

    def DeviceBright(self, device_type, device_name_tag, house_device_code, channel, bright_amount):
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

    def get_device_type(self, device_address, device_channel):
        """
        Return the type of device: plug, bulb, strip, etc.
        :param device_address:
        :param channel:
        :return:
        """
        return BaseDriverInterface.DEVICE_TYPE_PLUG

    # TODO Consider defining this as SetCurrentTime taking no parameters.
    # Set the controller time to the current, local time.
    def SetTime(self, time_value):
        raise NotImplementedError()

    # Reset the last error info
    def ClearLastError(self):
        self.LastErrorCode = 0
        self.LastError = None

    def hex_to_rgb(self, hex):
        """
        Convert #rrggbb to tuple(r,g,b).
        From: https://gist.github.com/matthewkremer/3295567
        :return:
        """
        hex = hex.lstrip('#')
        hlen = len(hex)
        return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))
