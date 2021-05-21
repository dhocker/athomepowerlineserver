#
# Kasa/TPLink device driver for TPLink/Kasa devices
# Based on python-kasa package: https://github.com/python-kasa/python-kasa
# © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from .base_driver_interface import BaseDriverInterface
from kasa import SmartPlug, SmartBulb, SmartStrip, SmartLightStrip, SmartDimmer, Discover
import asyncio
import logging

logger = logging.getLogger("server")


class PyKasaDriver(BaseDriverInterface):
    """
    Driver for TPLink/Kasa devices (SmartPlugs, SmartSwitch, SmartStrip, SmartBulb).
    Uses python-kasa package.
    """

    def __init__(self):
        """
        Initialize an instance of the python-kasa based driver
        """
        super().__init__()
        logger.info("PyKasa driver initialized")

    def open(self):
        """
        Open the driver. Does nothing for TPlink/Kasa devices.
        :return:
        """
        logger.debug("PyKasa driver opened")
        return True

    def close(self):
        """
        Close the driver. Does nothing for TPLink/Kasa devices.
        :return:
        """
        logger.debug("PyKasa driver closed")
        return True

    def set_color(self, device_type, device_name_tag, ip_address, channel, hex_color):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Device IP address
        :param channel: 0-n
        :param hex_color: Hex color #RRGGBB
        :return: True/false
        """
        result = False
        # TODO Requires a TPLink/Kasa bulb for testing
        logger.debug("set_color for: %s %s %s %s", device_type, device_name_tag, ip_address, channel)
        hsv = self.hex_to_hsv(hex_color)
        dev = self._create_smart_device(ip_address)
        if dev is not None and dev.is_color:
            self.clear_last_error()
            for r in range(5):
                try:
                    asyncio.run(dev.set_hsv(int(hsv[0]), int(hsv[1]), int(hsv[2])))
                    result = True
                    break
                except Exception as ex:
                    logger.error("Retry %d", r)
                    logger.error(str(ex))
                    self.LastError = str(ex)
                    self.LastErrorCode = 1
            del dev
        return result

    def set_brightness(self, device_type, device_name_tag, ip_address, channel, brightness):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Device address or UUID
        :param channel: 0-n
        :param brightness: 0-100 percent
        :return: True/false
        """
        result = False
        # TODO Requires a TPLink/Kasa bulb for testing
        logger.debug("set_brightness for: %s %s %s %s", device_type, device_name_tag, ip_address, channel)
        dev = self._create_smart_device(ip_address)
        if dev is not None and dev.is_dimmable:
            self.clear_last_error()
            for r in range(5):
                try:
                    asyncio.run(dev.brightness(int(brightness)))
                    result = True
                    break
                except Exception as ex:
                    logger.error("Retry %d", r)
                    logger.error(str(ex))
                    self.LastError = str(ex)
                    self.LastErrorCode = 1
            del dev
        return result

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
        if dev is not None:
            result = self._exec_device_function(dev.turn_on)
            del dev
        else:
            result = False
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
        if dev is not None:
            result = self._exec_device_function(dev.turn_off)
            del dev
        else:
            result = False
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
            devices = asyncio.run(Discover.discover())
            for ip, dev in devices.items():
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
        :param dev:
        :return: a dict with device attributes
        """
        attrs = {}
        try:
            sys_info = dev.sys_info
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
            elif isinstance(dev, SmartLightStrip):
                attrs["type"] = "LightStrip"
                attrs["channels"] = len(sys_info["children"])
            elif isinstance(dev, SmartDimmer):
                attrs["type"] = "Dimmer"
            else:
                attrs["type"] = "Unknown"
        except Exception as ex:
            logger.error("An exception occurred getting info for TPLink/Kasa device %s (%s)", dev.alias, dev.host)
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
                asyncio.run(device_function())
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
        # Try up to 5 times
        for retry in range(1, 6):
            try:
                device = asyncio.run(Discover.discover_single(ip_address))
                if device is None:
                    logger.error("Unable to discover TPLink device %s retry=%d", ip_address, retry)
                else:
                    return device
            except Exception as ex:
                logger.error("An exception occurred while discovering TPLink/Kasa device %s retry=%d", ip_address, retry)
                logger.error(str(ex))
                device = None

        return device