#
# Meross async i/o based driver
# Copyright © 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# This driver works with the meross-iot module at version 0.4+.
#

import asyncio
import time
from .base_driver_interface import BaseDriverInterface
from .meross_async_adapter import MerossAsyncAdapter
from Configuration import Configuration
import logging

logger = logging.getLogger("server")


class MerossDriverV4(BaseDriverInterface):
    MEROSS_ERROR = 7
    RETRY_COUNT = 5

    def __init__(self):
        self._async_adapter = MerossAsyncAdapter()
        # All async methods use this loop
        # TODO This is only good for the current thread. It won't work for requests
        # that come from API commands because they will be on different threads.
        self._loop = asyncio.get_event_loop()
        self._loop.set_debug(True)

        logger.info("Meross async adapter initialization started")
        super().__init__()
        logger.info("Meross async adapter initialized")

    @property
    def last_error_code(self):
        return self._async_adapter.last_error_code

    @last_error_code.setter
    def last_error_code(self, v):
        self._async_adapter.last_error_code = v

    @property
    def last_error(self):
        return self._async_adapter.last_error

    @last_error.setter
    def last_error(self, v):
        self._async_adapter.last_error = v

    # Open the device
    def open(self):
        # Starts the manager
        result = self._loop.run_until_complete(self._async_adapter.open(Configuration.MerossEmail(), Configuration.MerossPassword()))
        logger.info("Meross driver opened")

        return result

    # Close the device
    def close(self):
        result = self._loop.run_until_complete(self._async_adapter.close())
        self._loop.stop()
        self._loop.close()
        logger.info("Driver closed")

        return result

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
        rgb_color = self.hex_to_rgb(hex_color)
        result = self._loop.run_until_complete(self._async_adapter.set_color(device_type, device_name_tag,
                                                           house_device_code, channel, rgb_color))
        return result

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
        result = self._loop.run_until_complete(self._async_adapter.set_brightness(device_type, device_name_tag,
                                                                house_device_code, channel, brightness))
        return result

    def device_on(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param channel: 0-n
        :return:
        """
        result = self._loop.run_until_complete(self._async_adapter.device_on(device_type, device_name_tag,
                                                                house_device_code, channel))
        logger.debug("DeviceOn for: %s %s", house_device_code, channel)
        return result

    def device_off(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param dim_amount: a percent 0 to 100
        :return:
        """
        result = self._loop.run_until_complete(self._async_adapter.device_off(device_type, device_name_tag,
                                                                house_device_code, channel))
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

    def get_available_devices(self):
        """
        Get all known available devices for supported types.
        :return: Returns a dict where the key is the device UUID
        and the value is the human readable name of the device.
        """
        available_devices = self._async_adapter.get_available_devices()
        return available_devices

    def discover_devices(self):
        """
        Rescan for all Meross devices.
        :return:
        """
        self._loop.run_until_complete(self._async_adapter.discover_devices())

    #######################################################################
    # Set the controller time to the current, local time.
    def set_time(self, time_value):
        pass

    def get_device_type(self, device_address, device_channel):
        device_type = self._async_adapter.get_device_type(device_address, device_channel)
        return device_type
