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
import colorsys

logger = logging.getLogger("server")


class BaseDriverInterface:
    # Error codes
    SUCCESS = 0
    # Device types
    DEVICE_TYPE_PLUG = "plug"
    DEVICE_TYPE_BULB = "bulb"
    DEVICE_TYPE_STRIP = "strip"
    DEVICE_TYPE_LIGHTSTRIP = "lightstrip"
    DEVICE_TYPE_DIMMER = "dimmer"
    DEVICE_TYPE_UNKNOWN = "unknown"

    def __init__(self):
        self.clear_last_error()
        logger.info("Device driver base class initialized")

    @property
    def last_error_code(self):
        return self._last_error_code

    @last_error_code.setter
    def last_error_code(self, v):
        self._last_error_code = v

    @property
    def last_error(self):
        return self._last_error

    @last_error.setter
    def last_error(self, v):
        self._last_error = v

    def open(self):
        pass

    def close(self):
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

    def device_on(self, device_type, device_name_tag, house_device_code, channel):
        pass

    def device_off(self, device_type, device_name_tag, house_device_code, channel):
        pass

    def device_dim(self, device_type, device_name_tag, house_device_code, channel, dim_amount):
        pass

    def device_bright(self, device_type, device_name_tag, house_device_code, channel, bright_amount):
        pass

    def device_all_units_off(self, house_code):
        pass

    def device_all_lights_off(self, house_code):
        pass

    def device_all_lights_on(self, house_code):
        pass

    def get_available_devices(self):
        """
        Get all known available devices of a given type. Not every device can be discovered.
        For example TPLink/Kasa devices can be discovered, but X10 devices
        cannot be discovered.
        :return: Returns a dict where the key is the major device identifier or address
        and the value is the human readable name of the device.
        """
        return {}

    def discover_devices(self):
        """
        Discover all devices for this manufacturer
        :return:
        """
        pass

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
    def set_time(self, time_value):
        raise NotImplementedError()

    # Reset the last error info
    def clear_last_error(self):
        self.last_error_code = BaseDriverInterface.SUCCESS
        self.last_error = None

    def hex_to_rgb(self, hex_str):
        """
        Convert #rrggbb to tuple(r,g,b).
        From: https://gist.github.com/matthewkremer/3295567
        :param hex_str: hex representation of an RGB color #rrggbb 
        :return: rgb as a tuple(r,g,b)
        """
        hex_str = hex_str.lstrip('#')
        hlen = len(hex_str)
        return tuple(int(hex_str[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

    def hex_to_hsv(self, hex_str):
        """
        Convert #rrggbb to tuple(h,s,v)
        :param hex_str: hex representation of an RGB color #rrggbb 
        :return: hsv as a tuple(h,s,v)
        """
        rgb = self.hex_to_rgb(hex_str)
        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        return hsv