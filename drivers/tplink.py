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
from pyHS100 import SmartPlug, SmartBulb, SmartStrip
import logging

logger = logging.getLogger("server")

# Setup logging for the pyHS100 package
logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
logdateformat = '%Y-%m-%d %H:%M:%S'
loglevel = logging.DEBUG
# logging.basicConfig(level=loglevel, format=logformat, datefmt=logdateformat)


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
        dev.turn_on()
        del dev
        return True

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
        dev.turn_off()
        del dev
        return True

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

    def SetTime(self, time_value):
        pass

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