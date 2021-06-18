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

from .base_driver_interface import BaseDriverInterface
from .meross_adapter_thread import MerossAdapterThread
from .meross_request import MerossRequest
from Configuration import Configuration
import logging

logger = logging.getLogger("server")


class MerossDriverV4(BaseDriverInterface):
    MEROSS_ERROR = 7
    RETRY_COUNT = 5

    def __init__(self, request_wait_time=60.0):
        logger.info("Meross adapter thread initialization started")
        self._adapter_thread = MerossAdapterThread()
        # This is the current/last request
        self._request = MerossRequest()
        self._request_wait_time = request_wait_time
        super().__init__()
        logger.info("Meross adapter thread initialized")

    @property
    def last_error_code(self):
        return self._request.last_error_code

    @last_error_code.setter
    def last_error_code(self, v):
        self._request.last_error_code = v

    @property
    def last_error(self):
        return self._request.last_error

    @last_error.setter
    def last_error(self, v):
        self._request.last_error = v

    # Open the device
    def open(self):
        # Starts the Meross IOT interface thread
        self._adapter_thread.start()

        # Queue an open request
        kwargs = {
            "email": Configuration.MerossEmail(),
            "password": Configuration.MerossPassword()
        }
        self._request = MerossRequest(request=MerossRequest.OPEN, kwargs=kwargs)

        # Run the request on the adapter thread
        self._run_request(self._request)
        if self._request.result:
            logger.info("Meross adapter thread opened")
        else:
            logger.error("Meross open adapter thread failed")

        return self._request.result

    # Close the device
    def close(self):
        self._request = MerossRequest(request=MerossRequest.CLOSE)

        self._run_request(self._request)
        if self._request.result:
            logger.info("Meross adapter thread closed")
        else:
            logger.error("Meross close adapter thread timed out")

        # Wait for the adapter thread to terminate
        self._adapter_thread.join()
        logger.info("Driver closed")

        return self._request.result

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

        kwargs = {
            "device_type": device_type,
            "device_name_tag": device_name_tag,
            "house_device_code": house_device_code,
            "channel": channel,
            "rgb_color": rgb_color
        }

        # Queue a set color request
        self._request = MerossRequest(request=MerossRequest.SET_COLOR, kwargs=kwargs)
        self._run_request(self._request)

        return self._request.result

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

        kwargs = {
            "device_type": device_type,
            "device_name_tag": device_name_tag,
            "house_device_code": house_device_code,
            "channel": channel,
            "brightness": brightness
        }

        # Queue a set brightness request
        self._request = MerossRequest(request=MerossRequest.SET_BRIGHTNESS, kwargs=kwargs)
        self._run_request(self._request)

        return self._request.result

    def device_on(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param channel: 0-n
        :return:
        """

        kwargs = {
            "device_type": device_type,
            "device_name_tag": device_name_tag,
            "house_device_code": house_device_code,
            "channel": channel
        }

        # Queue a device on request
        self._request = MerossRequest(request=MerossRequest.DEVICE_ON, kwargs=kwargs)
        self._run_request(self._request)

        if self._request.result:
            logger.debug("Meross DeviceOn for: %s %s", house_device_code, channel)
        else:
            logger.error("Meross DeviceOn timed out")

        return self._request.result

    def device_off(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param channel: 0-n
        :return:
        """

        kwargs = {
            "device_type": device_type,
            "device_name_tag": device_name_tag,
            "house_device_code": house_device_code,
            "channel": channel
        }

        # Queue a device off request
        self._request = MerossRequest(request=MerossRequest.DEVICE_OFF, kwargs=kwargs)
        self._run_request(self._request)

        if self._request.result:
            logger.debug("Meross DeviceOff for: %s %s", house_device_code, channel)
        else:
            logger.error("Meross DeviceOn timed out")

        return self._request.result

    def device_dim(self, device_type, device_name_tag, house_device_code, channel, dim_amount):
        """
        Dim device
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: address of the device, depending on device type
        :param channel: 0-n
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
        :param channel: 0-n
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

        # Queue a get available devices request
        self._request = MerossRequest(request=MerossRequest.GET_AVAILABLE_DEVICES)
        self._run_request(self._request)

        return self._request.result

    def discover_devices(self):
        """
        Rescan for all Meross devices.
        :return:
        """

        # Queue a discover devices request
        self._request = MerossRequest(request=MerossRequest.DISCOVER_DEVICES)
        self._run_request(self._request)

        return self._request.result

    def get_device_type(self, device_address, device_channel):
        """
        Is it a bulb or a plug?
        :param device_address:
        :param device_channel:
        :return:
        """

        kwargs = {
            "device_address": device_address,
            "device_channel": device_channel
        }

        # Queue a get device type request
        self._request = MerossRequest(request=MerossRequest.GET_DEVICE_TYPE, kwargs=kwargs)
        self._run_request(self._request)

        return self._request.result

    def _run_request(self, request):
        """
        Queue a Meross device request to run on the adapter thread
        :param request:
        :return:
        """
        # Thread safe add to the adapter's request queue
        self._adapter_thread.queue_request(request)
        # Wait for the request to complete. This isn't an issue because most
        # of the time we are on a socket server thread.
        if request.wait(timeout=self._request_wait_time):
            logger.info("Meross request ran: %s", request.request)
        else:
            logger.error("Meross request timed out: %s", request.request)
