#
# TPLink device driver for TPLink/Kasa devices
# Copyright © 2019, 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from .base_driver_interface import BaseDriverInterface
from pyHS100 import SmartPlug, SmartBulb, SmartStrip, Discover
import logging

logger = logging.getLogger("server")


class TPLinkDriver(BaseDriverInterface):
    """
    Driver for TPLink/Kasa devices (SmartPlugs, SmartSwitch, SmartStrip, SmartBulb)
    """

    def __init__(self):
        super().__init__()
        logger.info("TPLink driver initialized")

    # Open the device
    def open(self):
        logger.debug("TPLink driver opened")

    # Close the device
    def close(self):
        logger.debug("TPLink driver closed")

    def set_color(self, device_type, device_name_tag, ip_address, channel, hex_color):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Device IP address
        :param channel: 0-n
        :param hex_color: Hex color #RRGGBB
        :return:
        """
        # TODO Requires a TPLink/Kasa bulb for testing
        logger.debug("set_color for: %s %s %s %s", device_type, device_name_tag, ip_address, channel)

    def set_brightness(self, device_type, device_name_tag, ip_address, channel, brightness):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Device address or UUID
        :param channel: 0-n
        :param brightness: 0-100 percent
        :return:
        """
        # TODO Requires a TPLink/Kasa bulb for testing
        logger.debug("set_brightness for: %s %s %s %s", device_type, device_name_tag, ip_address, channel)

    def device_on(self, device_type, device_name_tag, ip_address, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Smart device IP address
        :param channel: 0 to n
        :return:
        """
        logger.debug("DeviceOn for: %s %s %s %s", device_type, device_name_tag, ip_address, channel)
        dev = self._create_smart_device(ip_address)
        result = self._exec_device_function(dev.turn_on)
        del dev
        return result

    def device_off(self, device_type, device_name_tag, ip_address, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Smart device IP address
        :param channel: 0 to n
        :return:
        """
        logger.debug("DeviceOff for: %s %s %s %s", device_type, device_name_tag, ip_address, channel)
        dev = self._create_smart_device(ip_address)
        result = self._exec_device_function(dev.turn_off)
        del dev
        return result

    def device_dim(self, device_type, device_name_tag, ip_address, channel, dim_amount):
        logger.debug("DeviceDim for: %s %s %s", ip_address, channel, dim_amount)
        return True

    def device_bright(self, device_type, device_name_tag, ip_address, channel, bright_amount):
        logger.debug("DeviceBright for: %s %s %s", ip_address, channel, bright_amount)
        return True

    def device_all_units_off(self, house_code):
        logger.debug("DeviceAllUnitsOff for: %s", house_code)
        return True

    def device_all_lights_off(self, house_code):
        logger.debug("DeviceAllLightsOff for: %s", house_code)
        return True

    def device_all_lights_on(self, house_code):
        logger.debug("DeviceAllLightsOn for: %s", house_code)
        return True

    def get_available_devices(self):
        """
        Get all known available TPLink/Kasa devices.
        Reference: https://github.com/GadgetReactor/pyHS100
        :return: Returns a dict where the key is the device IP address
        and the value is the human readable name of the device.
        """
        try:
            result = {}
            # This can take a few seconds
            for ip, dev in Discover.discover().items():
                result[ip] = self._get_device_attrs(dev)
        except Exception as ex:
            logger.error("An exception occurred while trying to enumerate available TPLink/Kasa devices")
            logger.error(str(ex))

        return result

    def set_time(self, time_value):
        pass

    def _get_device_attrs(self, dev):
        """
        Get information for a TPLink device
        :param ip:
        :param dev:
        :return:
        """
        attrs = {}
        try:
            sys_info = dev.get_sysinfo()
            attrs["manufacturer"] ="TPLink"
            attrs["model"] = sys_info["model"]
            attrs["label"] = dev.alias
            attrs["channels"] = 1
            if isinstance(dev, SmartPlug):
                attrs["type"] = "Plug"
            elif isinstance(dev, SmartBulb):
                attrs["type"] = "Bulb"
            elif isinstance(dev, SmartStrip):
                attrs["type"] = "Strip"
                attrs["channels"] = len(sys_info["children"])
            else:
                attrs["type"] = "Unknown"
        except Exception as ex:
            logger.error("An exception occurred getting info for TPLink/Kasa device %s", ip)
            logger.error(str(ex))

        return attrs

    def _exec_device_function(self, device_function, retries=5):
        """
        Execute a device function with retries
        :param device_function: The function to be executed
        :param retries: The maximum number of attempts
        :return:
        """
        self.clear_last_error()
        for r in range(retries):
            try:
                device_function()
                return True
            except Exception as ex:
                logger.error("Retry %d", r)
                logger.error(str(ex))
                self.LastError = str(ex)
                self.LastErrorCode = 1

        return False

    @classmethod
    def _create_smart_device(cls, ip_address):
        """
        Create a TPLink SmartDevice instance for the device at a
        given IP address
        :param ip_address:
        :return:
        """
        device = Discover.discover_single(ip_address)
        if device is None:
            logger.error("Unable to discover TPLink device %s", ip_address)
        return device