#
# Adapter for meross-iot async module
# Copyright © 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import asyncio
# Reference: https://github.com/albertogeniola/MerossIot
# See also meross_asyncio_test.py
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager, RateLimitExceeded
from meross_iot.model.enums import OnlineStatus
import logging
import datetime

logger = logging.getLogger("server")


class MerossAsyncAdapter():
    # TODO Reconcile with base device driver definitions
    # Error codes
    SUCCESS = 0
    MEROSS_ERROR = 7
    RETRY_COUNT = 5
    # Device types
    DEVICE_TYPE_PLUG = "plug"
    DEVICE_TYPE_BULB = "bulb"
    DEVICE_TYPE_STRIP = "strip"

    def __init__(self):
        super().__init__()
        self._http_api_client = None
        self._manager = None
        self._last_error_code = 0
        self._last_error = None
        self._all_devices = None

    @property
    def last_error_code(self):
        return self._last_error_code

    @last_error_code.setter
    def last_error_code(self, v):
        self._last_error_code = v

    @property
    def last_error(self):
        return self._last_error

    @last_error.setter
    def last_error(self, v):
        self._last_error = v

    # Reset the last error info
    def clear_last_error(self):
        self.last_error_code = MerossAsyncAdapter.SUCCESS
        self.last_error = None

    async def _async_init(self, email, password):
        # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint.
        # There is an inordinate amount of retry code here. But, the Meross-iot package seems
        # go through a number of network errors when the server is started as part of a fresh boot-up.
        # There's probably a race condition where the network is not completely up.
        for retry in range(1, 11):
            try:
                logger.debug("Attempt %d to create a MerossManager instance", retry)
                # Initiates the Meross Cloud Manager.
                # This is in charge of handling the communication with the remote endpoint
                self._http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password)
                # What was learned by trial and error:
                # The design of the meross-iot module was targetted for smaller sets of devices (<10).
                # We have approx 20.
                # burst_requests_per_second_limit default value = 1 was too small for our 19 devices.
                # over_limit_threshold_percentage default of 400.0 was too small for a large number of devices.
                logger.debug("Creating Meross manager instance")
                self._manager = MerossManager(http_client=self._http_api_client,
                                        burst_requests_per_second_limit=3,  # default was 1
                                        over_limit_delay_seconds=1,
                                        over_limit_threshold_percentage=2000.0)  # default was 400.0

                # Starts the manager
                logger.debug("Meross driver calling async_init")
                await self._manager.async_init()
                logger.debug("Meross driver initialized")
                return True
            except Exception as ex:
                logger.error("Unhandled exception attempting to create a MerossManager instance")
                logger.error("Exception type is %s", type(ex))
                # Wait incrementally longer for network to settle
                logger.debug("Waiting %d second(s) to retry", retry)
                await asyncio.sleep(float(retry))

        logger.error("After 10 retries, unable to create MerossManager instance")
        return False

    # Open the device
    async def open(self, email, password):
        """
        Open the meross-iot manager
        :param email:
        :param password:
        :return:
        """
        self.clear_last_error()
        try:
            result = await self._async_init(email, password)
            # For now, discover all devices.
            await self.discover_devices()
            logger.info("Meross driver adapter opened")
            return result
        except Exception as ex:
            logger.error("Exception during manager.start()")
            logger.error(str(ex))
            self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
            self.last_error = str(ex)
        return False

    async def close(self):
        """
        Close the meross-iot manager
        :return:
        """
        self.clear_last_error()
        try:
            if self._manager:
                logger.debug("Closing meross-iot manager instance")
                self._manager.close()
            if self._http_api_client:
                logger.debug("Logging out from meross-iot http client service")
                await self._http_api_client.async_logout()
            logger.info("Meross driver adapter closed")
            return True
        except Exception as ex:
            logger.error("Exception during manager.stop()")
            logger.error(str(ex))
            self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
            self.last_error = str(ex)
        return False

    async def set_color(self, device_type, device_name_tag, house_device_code, channel, rgb_color):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Device address or UUID
        :param channel: 0-n
        :param rgb_color: color as an (r,g,b) tuple
        :return:
        """
        self.clear_last_error()
        for retry in range(MerossAsyncAdapter.RETRY_COUNT):
            try:
                device = self._get_device(house_device_code)
                await device.async_update()
                # Currently, a bulb is the only Meross device that supports color
                if self._supports_color(device):
                    await device.async_set_light_color(channel=channel, rgb=rgb_color)
                else:
                   return False
                logger.debug("set_color for: %s (%s %s) %s", device_name_tag, house_device_code, channel, rgb_color)
                return True
            except Exception as ex:
                logger.error("Exception during set_color for: %s (%s %s) %s",
                             device_name_tag, house_device_code, channel, rgb_color)
                logger.error(str(ex))
                self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
                self.last_error = str(ex)
                # Clean up device instance
                del device
                device = None
                # TODO Restart the Meross manager
                # self._restart_manager()
            finally:
                pass

        return False

    async def set_brightness(self, device_type, device_name_tag, house_device_code, channel, brightness):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Device address or UUID
        :param channel: 0-n
        :param brightness: 0-100 percent
        :return:
        """
        self.clear_last_error()
        for retry in range(MerossAsyncAdapter.RETRY_COUNT):
            try:
                device = self._get_device(house_device_code)
                await device.async_update()
                # Currently, a bulb is the only Meross device that supports brightness
                if self._supports_brightness(device):
                    await device.async_set_light_color(channel=channel, luminance=brightness)
                else:
                   return False
                logger.debug("set_brightness for: %s (%s %s) %s",
                             device_name_tag, house_device_code, channel, brightness)
                return True
            except Exception as ex:
                logger.error("Exception during set_brightness for: %s (%s %s) %s",
                             device_name_tag, house_device_code, channel, brightness)
                logger.error(str(ex))
                self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
                self.last_error = str(ex)
                # Clean up device instance
                del device
                device = None
                # TODO Restart the Meross manager
                # self._restart_manager()
            finally:
                pass

        return False

    async def device_on(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: the UUID of the Meross device
        :param channel: 0-n
        :return:
        """
        self.clear_last_error()
        for retry in range(MerossAsyncAdapter.RETRY_COUNT):
            try:
                device = self._get_device(house_device_code)
                await device.async_turn_on(channel)
                logger.debug("DeviceOn for: %s (%s %s)", device_name_tag, house_device_code, channel)
                return True
            except Exception as ex:
                logger.error("Exception during DeviceOn for: %s (%s %s)", device_name_tag, house_device_code, channel)
                logger.error(str(ex))
                self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
                self.last_error = str(ex)
                # Clean up device instance
                del device
                device = None
                # TODO Restart the Meross manager
                # self._restart_manager()
            finally:
                pass

        return False

    async def device_off(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: the UUID of the Meross device
        :param channel: 0-n
        :return:
        """
        self.clear_last_error()
        for retry in range(MerossAsyncAdapter.RETRY_COUNT):
            try:
                device = self._get_device(house_device_code)
                await device.async_turn_off(channel)
                logger.debug("DeviceOff for: %s (%s %s)", device_name_tag, house_device_code, channel)
                return True
            except Exception as ex:
                logger.error("Exception during DeviceOff for: %s (%s %s)", device_name_tag, house_device_code, channel)
                logger.error(str(ex))
                self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
                self.last_error = str(ex)
                # Clean up device instance
                del device
                device = None
                # TODO Restart the Meross manager
                # self._restart_manager()
            finally:
                pass

        return False

    def get_available_devices(self):
        """
        Get all known available devices for supported types.
        :return: Returns a dict where the key is the device UUID
        and the value is a dict of device attributes/properties.
        """
        start_time = datetime.datetime.now()

        available_devices = {}
        try:
            for device in self._all_devices:
                available_devices[device.uuid] = self._build_device_details(device)
        except Exception as ex:
            logger.error("Exception enumerating available devices")
            logger.error(str(ex))
            self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
            self.last_error = str(ex)
        finally:
            pass

        elapsed_time = datetime.datetime.now() - start_time
        logger.debug("get_available_devices elapsed time: %f", elapsed_time.total_seconds())
        return available_devices

    async def discover_devices(self):
        """
        Discover all Meross devices register to the account. This is
        equivalent to rescan devices.
        :return:
        """
        logger.debug("Discovering Meross devices")
        # For now, discover all devices. This takes about 1 sec per device.
        await self._manager.async_device_discovery(update_subdevice_status=False)

        # Find and update ALL devices
        self._all_devices = self._manager.find_devices()
        for device in self._all_devices:
            # This update takes about 1 sec per device
            await device.async_update()

    def get_device_type(self, device_address, device_channel):
        device = self._get_device(device_address)
        if device.type.lower().startswith("msl"):
            return MerossAsyncAdapter.DEVICE_TYPE_BULB
        else:
            return MerossAsyncAdapter.DEVICE_TYPE_PLUG

    #######################################################################
    # Set the controller time to the current, local time.
    def set_time(self, time_value):
        pass

    def _restart_manager(self):
        """
        Restart the Meross communication manager
        :return:
        """
        logger.debug("Restarting Meross communication manager")
        self._manager.stop()
        self._manager.start()

    def _get_device(self, device_uuid):
        """
        Return the device instance for a given device.
        :param device_uuid: UUID of device
        :return: Device instance or None
        """
        device = None
        for retry in range(MerossAsyncAdapter.RETRY_COUNT):
            try:
                devices = self._manager.find_devices(device_uuids=[device_uuid])
                device = devices[0]
                return device
            except Exception as ex:
                logger.error("Exception attempting to get Meross device instance for %s", device_uuid)
                logger.error(str(ex))
                self.last_error_code = MerossAsyncAdapter.MEROSS_ERROR
                self.last_error = str(ex)
                # TODO Restart the Meross manager
                # self._restart_manager()
            finally:
                pass

        return device

    def _build_device_details(self, dd):
        """
        Build a device details dictionary for a device
        :param dd: GenericPlug, GenericBulb, etc.
        :return: Details dict
        """
        attrs = {"manufacturer": "Meross"}
        attrs["online"] = dd.online_status == OnlineStatus.ONLINE
        attrs["model"] = dd.type
        # A plug or switch
        if dd.type.lower().startswith("mss"):
            attrs["type"] = MerossAsyncAdapter.DEVICE_TYPE_PLUG
            channels = len(dd.channels)
            attrs["channels"] = channels
            device_label = "{0} [{1} channel(s)]".format(dd.name, channels)
            attrs["label"] = device_label
            attrs["usb"] = False
        # A bulb supporting color and luminance
        elif dd.type.lower().startswith("msl"):
            attrs["type"] = MerossAsyncAdapter.DEVICE_TYPE_BULB
            attrs["channels"] = 1
            attrs["label"] = dd.name
            attrs["usb"] = False
            if dd.online_status == OnlineStatus.ONLINE:
                # These attributes are only available if the device is online
                attrs["rgb"] = dd.get_supports_rgb()
                attrs["temperature"] = dd.get_supports_temperature()
                attrs["luminance"] = dd.get_supports_luminance()
            else:
                attrs["rgb"] = False
                attrs["temperature"] = False
                attrs["luminance"] = False
        else:
            attrs["type"] = "Unknown"
            device_label = dd.name

        return attrs

    def _supports_color(self, device):
        """
        Somewhat risky test to see if a device supports color
        :param device:
        :return:
        """
        a = getattr(device, "get_supports_rgb", None)
        return not a is None

    def _supports_brightness(self, device):
        """
        Somewhat risky test to see if a device supports brightness
        :param device:
        :return:
        """
        a = getattr(device, "get_supports_luminance", None)
        return not a is None
