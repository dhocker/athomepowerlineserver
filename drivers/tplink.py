#
# TPLink device driver for TPLink/Kasa devices
# Copyright © 2019  Dave Hocker
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
    def Open(self):
        logger.debug("TPLink driver opened")

    # Close the device
    def Close(self):
        logger.debug("TPLink driver closed")

    def DeviceOn(self, device_type, device_name_tag, ip_address, dim_amount):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Smart device IP address
        :param dim_amount: 0 to 100
        :return:
        """
        logger.debug("DeviceOn for: %s %s %s %s", device_type, device_name_tag, ip_address, dim_amount)
        dev = self._create_smart_device(device_type, ip_address)
        result = self._exec_device_function(dev.turn_on)
        del dev
        return result

    def DeviceOff(self, device_type, device_name_tag, ip_address, dim_amount):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param ip_address: Smart device IP address
        :param dim_amount: 0 to 100
        :return:
        """
        logger.debug("DeviceOff for: %s %s %s %s", device_type, device_name_tag, ip_address, dim_amount)
        dev = self._create_smart_device(device_type, ip_address)
        result = self._exec_device_function(dev.turn_off)
        del dev
        return result

    def DeviceDim(self, device_type, device_name_tag, ip_address, dim_amount):
        logger.debug("DeviceDim for: %s %s", ip_address, dim_amount)
        return True

    def DeviceBright(self, device_type, device_name_tag, ip_address, bright_amount):
        logger.debug("DeviceBright for: %s %s", ip_address, bright_amount)
        return True

    def DeviceAllUnitsOff(self, house_code):
        logger.debug("DeviceAllUnitsOff for: %s", house_code)
        return True

    def DeviceAllLightsOff(self, house_code):
        logger.debug("DeviceAllLightsOff for: %s", house_code)
        return True

    def DeviceAllLightsOn(self, house_code):
        logger.debug("DeviceAllLightsOn for: %s", house_code)
        return True

    def GetAvailableDevices(self):
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
                attrs = {"manufacturer": "TPLink/Kasa"}
                attrs["label"] = dev.alias
                if isinstance(dev, SmartPlug):
                    attrs["type"] = "Plug"
                elif isinstance(dev, SmartBulb):
                    attrs["type"] = "Bulb"
                elif isinstance(dev, SmartStrip):
                    attrs["type"] = "Strip"
                else:
                    attrs["type"] = "Unknown"
                result[ip] = attrs
        except Exception as ex:
            logger.error("An exception occurred while trying to enumerate available TPLink/Kasa devices")
            logger.error(str(ex))
            result = {}

        return result

    def SetTime(self, time_value):
        pass

    def _exec_device_function(self, device_function, retries=5):
        """
        Execute a device function with retries
        :param device_function: The function to be executed
        :param retries: The maximum number of attempts
        :return:
        """
        self.ClearLastError()
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

    TPLINK_DEVICE_LIST = {
        "tplink": SmartPlug,
        "hs100": SmartPlug,
        "hs103": SmartPlug,
        "hs105": SmartPlug,
        "hs107": SmartPlug,
        "smartplug": SmartPlug,
        "smartswitch": SmartPlug,
        "smartbulb": SmartBulb,
        "smartstrip": SmartStrip
    }

    @classmethod
    def _create_smart_device(cls, device_type, ip_address):
        if device_type in cls.TPLINK_DEVICE_LIST.keys():
            return cls.TPLINK_DEVICE_LIST[device_type](ip_address)
        # Default to smart plug
        return SmartPlug(ip_address)