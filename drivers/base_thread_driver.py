#
# async i/o base driver
# Copyright © 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# This driver works with the meross-iot module at version 0.4+
# and the python-kasa module at version 0.4.0.dev2+.
#

from .base_driver_interface import BaseDriverInterface
from .adapter_request import AdapterRequest
import logging
import datetime

logger = logging.getLogger("server")


class BaseThreadDriver(BaseDriverInterface):
    DRIVER_ERROR = 7
    RETRY_COUNT = 5

    def __init__(self, adapter_thread=None, request_wait_time=60.0):
        logger.info("BaseThreadDriver initialization started")
        self._adapter_thread = adapter_thread
        # This is the current/last request
        self._request = AdapterRequest()
        self._request_wait_time = request_wait_time
        super().__init__()
        logger.info("%s BaseThreadDriver initialized", self._adapter_thread.adapter_name)

        # Starts the adapter thread
        logger.debug("Starting %s", adapter_thread.adapter_name)
        self._adapter_thread.start()

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
    def open(self, kwargs=None):
        """
        Open the thread-based adapter
        :param kwargs: Usually an email/ID and password
        :return: True or False
        """
        # Queue an open request
        self._request = AdapterRequest(request=AdapterRequest.OPEN, kwargs=kwargs)

        # Run the request on the adapter thread
        self._run_request(self._request)
        if self._request.result:
            logger.debug("%s opened", self._adapter_thread.adapter_name)
        else:
            logger.error("%s failed", self._adapter_thread.adapter_name)

        return self._request.result

    # Close the device
    def close(self):
        logger.info("%s has %d requests queued",
                    self._adapter_thread.adapter_name,
                    self._adapter_thread.queued_requests())

        self._request = AdapterRequest(request=AdapterRequest.CLOSE)

        self._run_request(self._request)
        if self._request.result:
            logger.debug("%s closed", self._adapter_thread.adapter_name)
        else:
            logger.error("%s close timed out", self._adapter_thread.adapter_name)

        # Wait for the adapter thread to terminate
        logger.debug("Waiting for %s driver adapter thread to terminate", self._adapter_thread.adapter_name)
        self._adapter_thread.join()
        logger.debug("%s driver adapter thread ended", self._adapter_thread.adapter_name)

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

        kwargs = {
            "device_type": device_type,
            "device_name_tag": device_name_tag,
            "house_device_code": house_device_code,
            "channel": channel,
            "hex_color": hex_color
        }

        # Queue a set color request
        self._request = AdapterRequest(request=AdapterRequest.SET_COLOR, kwargs=kwargs)
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
        self._request = AdapterRequest(request=AdapterRequest.SET_BRIGHTNESS, kwargs=kwargs)
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
        self._request = AdapterRequest(request=AdapterRequest.DEVICE_ON, kwargs=kwargs)
        self._run_request(self._request)

        if self._request.result:
            logger.debug("%s DeviceOn for: %s %s", self._adapter_thread.adapter_name, house_device_code, channel)
        else:
            logger.error("%s DeviceOn timed out", self._adapter_thread.adapter_name)

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
        self._request = AdapterRequest(request=AdapterRequest.DEVICE_OFF, kwargs=kwargs)
        self._run_request(self._request)

        if self._request.result:
            logger.debug("%s DeviceOff for: %s %s", self._adapter_thread.adapter_name, house_device_code, channel)
        else:
            logger.error("%s DeviceOff timed out", self._adapter_thread.adapter_name)

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
        logger.debug("%s DeviceDim for: %s %s %s", self._adapter_thread.adapter_name,
                     house_device_code, channel, dim_amount)
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
        logger.debug("%s DeviceBright for: %s %s %s", self._adapter_thread.adapter_name,
                     house_device_code, channel, bright_amount)
        return True

    def device_all_units_off(self, house_code):
        """
        Turn all units off. Not implemented by all device types.
        :param house_code:
        :return:
        """
        logger.debug("%s DeviceAllUnitsOff for: %s", self._adapter_thread.adapter_name, house_code)
        return True

    def device_all_lights_off(self, house_code):
        """
        Turn all lights off. Not implemented by all device types.
        :param house_code:
        :return:
        """
        logger.debug("%s DeviceAllLightsOff for: %s", self._adapter_thread.adapter_name, house_code)
        return True

    def device_all_lights_on(self, house_code):
        """
        Turn all lights on. Not implemented by all device types
        :param house_code:
        :return:
        """
        logger.debug("%s DeviceAllLightsOn for: %s", self._adapter_thread.adapter_name, house_code)
        return True

    def get_available_devices(self):
        """
        Get all known available devices for supported types.
        :return: Returns a dict where the key is the device UUID
        and the value is the human readable name of the device.
        """

        # Queue a get available devices request
        self._request = AdapterRequest(request=AdapterRequest.GET_AVAILABLE_DEVICES)
        self._run_request(self._request)

        return self._request.result

    def discover_devices(self):
        """
        Rescan for all Meross devices.
        :return:
        """

        # Queue a discover devices request
        self._request = AdapterRequest(request=AdapterRequest.DISCOVER_DEVICES)
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
        self._request = AdapterRequest(request=AdapterRequest.GET_DEVICE_TYPE, kwargs=kwargs)
        self._run_request(self._request)

        return self._request.result

    def is_on(self, device_address, device_channel):
        """
        Is it a device on?
        :param device_address:
        :param device_channel:
        :return:
        """

        kwargs = {
            "device_address": device_address,
            "device_channel": device_channel
        }

        # Queue a on/off status request
        self._request = AdapterRequest(request=AdapterRequest.ON_OFF_STATUS, kwargs=kwargs)
        self._run_request(self._request)

        return self._request.result

    def _run_request(self, request):
        """
        Queue a Meross device request to run on the adapter thread
        :param request:
        :return:
        """
        # Thread safe add to the adapter thread's request queue
        self._adapter_thread.queue_request(request)

        # Wait for the request to complete. This isn't an issue because most
        # of the time we are on a socket server thread.
        start_wait = datetime.datetime.now()
        if request.wait(timeout=self._request_wait_time):
            logger.info("%s request ran: %s", self._adapter_thread.adapter_name, request.request)
        else:
            wait_time = datetime.datetime.now() - start_wait
            logger.error("%s %s timed out after %f sec",
                         self._adapter_thread.adapter_name,
                         request.request,
                         wait_time.total_seconds())
