#
# Dummy device driver that works for all devices
# Copyright © 2014, 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import drivers.X10ControllerInterface as X10ControllerInterface
from .base_driver_interface import BaseDriverInterface
import logging

logger = logging.getLogger("server")


class Dummy(BaseDriverInterface):

    def __init__(self):
        super().__init__()
        logger.info("Dummy driver initialized")
        pass

    # Open the device
    def Open(self):
        logger.debug("Driver opened")

    # Close the device
    def Close(self):
        logger.debug("Driver closed")

    def DeviceOn(self, device_type, device_name_tag, house_device_code, dim_amount):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param dim_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceOn for: %s %s", house_device_code, dim_amount)
        return True

    def DeviceOff(self, device_type, device_name_tag, house_device_code, dim_amount):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param dim_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceOff for: %s %s", house_device_code, dim_amount)
        return True

    def DeviceDim(self, device_type, device_name_tag, house_device_code, dim_amount):
        """
        Dim device
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param dim_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceDim for: %s %s", house_device_code, dim_amount)
        return True

    def DeviceBright(self, device_type, device_name_tag, house_device_code, bright_amount):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param bright_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceBright for: %s %s", house_device_code, bright_amount)
        return True

    def DeviceAllUnitsOff(self, house_code):
        """
        Turn all units off. Not implemented by all device types.
        :param house_code:
        :return:
        """
        logger.debug("DeviceAllUnitsOff for: %s", house_code)
        return True

    def DeviceAllLightsOff(self, house_code):
        """
        Turn all lights off. Not implemented by all device types.
        :param house_code:
        :return:
        """
        logger.debug("DeviceAllLightsOff for: %s", house_code)
        return True

    def DeviceAllLightsOn(self, house_code):
        """
        Turn all lights on. Not implemented by all device types
        :param house_code:
        :return:
        """
        logger.debug("DeviceAllLightsOn for: %s", house_code)
        return True

    #######################################################################
    # Set the controller time to the current, local time.
    def SetTime(self, time_value):
        pass
