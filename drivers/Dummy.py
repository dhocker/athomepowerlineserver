#
# Dummy device driver that works for all devices
# Copyright © 2014, 2020  Dave Hocker
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
    def open(self):
        logger.debug("Driver opened")

    # Close the device
    def close(self):
        logger.debug("Driver closed")

    def device_on(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param dim_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceOn for: %s %s", house_device_code, channel)
        return True

    def device_off(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param dim_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceOff for: %s %s", house_device_code, channel)
        return True

    def device_dim(self, device_type, device_name_tag, house_device_code, channel, dim_amount):
        """
        Dim device
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param dim_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceDim for: %s %s %s", house_device_code, channel, dim_amount)
        return True

    def device_bright(self, device_type, device_name_tag, house_device_code, channel, bright_amount):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param bright_amount: a percent 0 to 100
        :return:
        """
        logger.debug("DeviceBright for: %s %s %s", house_device_code, channel, bright_amount)
        return True

    def device_all_units_off(self, house_code):
        """
        Turn all units off. Not implemented by all device types.
        :param house_code:
        :return:
        """
        logger.debug("DeviceAllUnitsOff for: %s", house_code)
        return True

    def device_all_lights_off(self, house_code):
        """
        Turn all lights off. Not implemented by all device types.
        :param house_code:
        :return:
        """
        logger.debug("DeviceAllLightsOff for: %s", house_code)
        return True

    def device_all_lights_on(self, house_code):
        """
        Turn all lights on. Not implemented by all device types
        :param house_code:
        :return:
        """
        logger.debug("DeviceAllLightsOn for: %s", house_code)
        return True

    #######################################################################
    # Set the controller time to the current, local time.
    def set_time(self, time_value):
        pass
