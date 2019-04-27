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
from pyHS100 import SmartPlug
import logging

logger = logging.getLogger("server")

# Setup logging for the pyHS100 package
logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
logdateformat = '%Y-%m-%d %H:%M:%S'
loglevel = logging.DEBUG
logging.basicConfig(level=loglevel, format=logformat, datefmt=logdateformat)


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

    def DeviceOn(self, ip_address, dim_amount):
        """
        Turn device on
        :param ip_address: Smart device IP address
        :param dim_amount: 0 to 100
        :return:
        """
        logger.debug("DeviceOn for: %s %s", ip_address, dim_amount)
        dev = SmartPlug(ip_address)
        dev.turn_on()
        del dev
        return True

    def DeviceOff(self, ip_address, dim_amount):
        logger.debug("DeviceOff for: %s %s", ip_address, dim_amount)
        dev = SmartPlug(ip_address)
        dev.turn_off()
        del dev
        return True

    def DeviceDim(self, ip_address, dim_amount):
        logger.debug("DeviceDim for: %s %s", ip_address, dim_amount)
        return True

    def DeviceBright(self, ip_address, bright_amount):
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
