#
# Thread based adapter for meross-iot async module
# Copyright © 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# Reference: https://github.com/albertogeniola/MerossIot
# See also meross_asyncio_test.py
#
# The Meross-iot module makes significant use of asyncio. asyncio has a
# number of limitations that make it somewhat difficult to deal with in
# a multi-threaded application.
# The asyncio documentation itself explicitly states that it is not
# inherently thread safe. It appears to have been designed to run
# on the main thread.
#
# The athomeserver uses multiple threads.
# For example, each network connection (read incoming command) arrives on its
# own thread. The timer program thread checks and triggers timer programs.
# Device drivers are initialized on the main thread.
#
# This means that all Meross-iot code must be isolated to a single thread.
# Otherwise, asyncio will throw thread related exceptions when least expected.
#
# This adapter is inherently thread safe. The request queue (a Queue) is used as the
# synchronization method. A Queue is thread safe (see Queue.put and Queue.get).
# The adapter takes/gets one request at a time from the request queue making it
# thread safe.
#

import asyncio
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.model.enums import OnlineStatus
import logging
from .adapter_thread import AdapterThread
from .adapter_request import AdapterRequest

logger = logging.getLogger("server")


class MerossAdapterThread(AdapterThread):
    # TODO Reconcile with base device driver definitions
    # Error codes
    SUCCESS = 0
    MEROSS_ERROR = 7
    RETRY_COUNT = 5

    def __init__(self, name="MerossAdapterThread"):
        super().__init__(name=name)
        self._http_api_client = None
        self._manager = None
        self._all_devices = None

    def dispatch_request(self):
        """
        Dispatch an adapter request.
        This method is called on the new thread by the base class run method.
        The server terminates when the close request is received.
        :return: Returns the result from running the request.
        """
        result = None

        # Cases for each request/command
        if self._request.request == AdapterRequest.DEVICE_ON:
            result = self._loop.run_until_complete(self.device_on(**self._request.kwargs))
        elif self._request.request == AdapterRequest.DEVICE_OFF:
            result = self._loop.run_until_complete(self.device_off(**self._request.kwargs))
        elif self._request.request == AdapterRequest.SET_BRIGHTNESS:
            result = self._loop.run_until_complete(self.set_brightness(**self._request.kwargs))
        elif self._request.request == AdapterRequest.SET_COLOR:
            result = self._loop.run_until_complete(self.set_color(**self._request.kwargs))
        elif self._request.request == AdapterRequest.OPEN:
            result = self._loop.run_until_complete(self.open(**self._request.kwargs))
        elif self._request.request == AdapterRequest.CLOSE:
            result = self._loop.run_until_complete(self.close())
        elif self._request.request == AdapterRequest.GET_DEVICE_TYPE:
            # NOT an asyncio method
            result = self.get_device_type(**self._request.kwargs)
        elif self._request.request == AdapterRequest.GET_AVAILABLE_DEVICES:
            # NOT an asyncio method
            result = self.get_available_devices()
        elif self._request.request == AdapterRequest.DISCOVER_DEVICES:
            result = self._loop.run_until_complete(self.discover_devices())
        elif self._request.request == AdapterRequest.ON_OFF_STATUS:
            # Currently NOT an asyncio method
            result = self.is_on(**self._request.kwargs)
        else:
            logger.error("Unrecognized request: %s", self._request.request)
            result = False

        return result

    async def _async_init(self, email, password):
        """
        Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint.
        There is an inordinate amount of retry code here. But, the Meross-iot package seems
        go through a number of network errors when the server is started as part of a fresh boot-up.
        There's probably a race condition where the network is not completely up.
        :param email:
        :param password:
        :return:
        """
        for retry in range(1, 11):
            try:
                logger.debug("Attempt %d to create a MerossManager instance", retry)
                # Initiates the Meross Cloud Manager.
                # This is in charge of handling the communication with the Meross cloud (MQTT service)
                self._http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password)
                # What was learned by trial and error:
                # The design of the meross-iot module was targeted for smaller sets of devices (<10).
                # We have more than 20.
                # burst_requests_per_second_limit default value = 1 was too small for our 19 devices.
                # over_limit_threshold_percentage default of 400.0 was too small for a large number of devices.
                logger.debug("Creating Meross manager instance")
                self._manager = MerossManager(http_client=self._http_api_client,
                                              loop=self._loop,
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
            self.last_error_code = MerossAdapterThread.MEROSS_ERROR
            self.last_error = str(ex)
        return False

    async def close(self):
        """
        Close the meross-iot manager
        :return:
        """
        self.clear_last_error()
        result = False
        try:
            if self._manager:
                logger.debug("Closing meross-iot manager instance")
                self._manager.close()
            if self._http_api_client:
                logger.debug("Logging out from meross-iot http client service")
                await self._http_api_client.async_logout()
            logger.info("Meross adapter thread closed")
            result = True
        except Exception as ex:
            logger.error("Exception during manager.stop()")
            logger.error(str(ex))
            self.last_error_code = MerossAdapterThread.MEROSS_ERROR
            self.last_error = str(ex)
        finally:
            # Unconditionally, the adapter thread will terminate
            self._terminate_event.set()

        return result

    async def set_color(self, device_type, device_name_tag, house_device_code, channel, hex_color):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Device address or UUID
        :param channel: 0-n
        :param hex_color: color as an (r,g,b) tuple
        :return:
        """
        self.clear_last_error()

        rgb_color = self._hex_to_rgb(hex_color)

        for retry in range(MerossAdapterThread.RETRY_COUNT):
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
                self.last_error_code = MerossAdapterThread.MEROSS_ERROR
                self.last_error = str(ex)
                # Clean up device instance
                del device
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
        for retry in range(MerossAdapterThread.RETRY_COUNT):
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
                self.last_error_code = MerossAdapterThread.MEROSS_ERROR
                self.last_error = str(ex)
                # Clean up device instance
                del device
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
        result = False
        for retry in range(MerossAdapterThread.RETRY_COUNT):
            try:
                device = self._get_device(house_device_code)
                await device.async_turn_on(channel)
                logger.debug("DeviceOn for: %s (%s %s)", device_name_tag, house_device_code, channel)
                result = True
                break
            except Exception as ex:
                logger.error("Exception during DeviceOn for: %s (%s %s)", device_name_tag, house_device_code, channel)
                logger.error(str(ex))
                self.last_error_code = MerossAdapterThread.MEROSS_ERROR
                self.last_error = str(ex)
            finally:
                pass

        return result

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
        result = False
        for retry in range(MerossAdapterThread.RETRY_COUNT):
            try:
                device = self._get_device(house_device_code)
                await device.async_turn_off(channel)
                logger.debug("DeviceOff for: %s (%s %s)", device_name_tag, house_device_code, channel)
                result = True
                break
            except Exception as ex:
                logger.error("Exception during DeviceOff for: %s (%s %s)", device_name_tag, house_device_code, channel)
                logger.error(str(ex))
                self.last_error_code = MerossAdapterThread.MEROSS_ERROR
                self.last_error = str(ex)
            finally:
                pass

        return result

    def get_available_devices(self):
        """
        Get all known available devices for supported types.
        :return: Returns a dict where the key is the device UUID
        and the value is a dict of device attributes/properties.
        """
        available_devices = {}
        try:
            for device in self._all_devices:
                available_devices[device.uuid] = self._build_device_details(device)
        except Exception as ex:
            logger.error("Exception enumerating available devices")
            logger.error(str(ex))
            self.last_error_code = MerossAdapterThread.MEROSS_ERROR
            self.last_error = str(ex)
        finally:
            pass

        return available_devices

    async def discover_devices(self):
        """
        Discover all Meross devices registered to the account. This is
        equivalent to rescanning devices.
        :return:
        """
        logger.debug("Discovering Meross devices")
        # For now, discover all devices. This takes about 1 sec per device.
        await self._manager.async_device_discovery(update_subdevice_status=False)
        logger.debug("All Meross devices discovered")

        # Find and update ALL devices
        logger.debug("Updating all discovered Meross devices")
        self._all_devices = self._manager.find_devices()
        for device in self._all_devices:
            # This update takes about 1 sec per device
            await device.async_update()
        logger.debug("All discovered Meross devices have been updated")

        return True

    def get_device_type(self, device_address, device_channel):
        """
        Determine the type of a given device
        :param device_address:
        :param device_channel: 0-n
        :return: Either plug or bulb.
        """
        device = self._get_device(device_address)
        if device.type.lower().startswith("msl"):
            return MerossAdapterThread.DEVICE_TYPE_BULB
        # The default
        return MerossAdapterThread.DEVICE_TYPE_PLUG

    def is_on(self, device_address, device_channel):
        """
        Determine the on/off status of a device
        :param device_address:
        :param device_channel: 0-n
        :return: True if the device is on.
        """
        device = self._get_device(device_address)
        if hasattr(device, "is_on"):
            return device.is_on()
        return False

    def _get_device(self, device_uuid):
        """
        Return the device instance for a given device.
        :param device_uuid: UUID of device
        :return: Device instance or None
        """
        device = None
        for retry in range(MerossAdapterThread.RETRY_COUNT):
            try:
                devices = self._manager.find_devices(device_uuids=[device_uuid])
                device = devices[0]
                return device
            except Exception as ex:
                logger.error("Exception attempting to get Meross device instance for %s", device_uuid)
                logger.error(str(ex))
                self.last_error_code = MerossAdapterThread.MEROSS_ERROR
                self.last_error = str(ex)
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
            attrs["type"] = MerossAdapterThread.DEVICE_TYPE_PLUG
            channels = len(dd.channels)
            attrs["channels"] = channels
            device_label = "{0} [{1} channel(s)]".format(dd.name, channels)
            attrs["label"] = device_label
            attrs["usb"] = False
        # A bulb supporting color and luminance
        elif dd.type.lower().startswith("msl"):
            attrs["type"] = MerossAdapterThread.DEVICE_TYPE_BULB
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
            attrs["label"] = dd.name

        return attrs

    def _supports_color(self, device):
        """
        Somewhat risky test to see if a device supports color
        :param device:
        :return:
        """
        a = getattr(device, "get_supports_rgb", None)
        return a is not None

    def _supports_brightness(self, device):
        """
        Somewhat risky test to see if a device supports brightness
        :param device:
        :return:
        """
        a = getattr(device, "get_supports_luminance", None)
        return a is not None
