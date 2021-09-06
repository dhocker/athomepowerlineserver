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
from datetime import timedelta, datetime
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager, CommandTimeoutError
from meross_iot.model.enums import OnlineStatus
from meross_iot.utilities.limiter import RateLimitChecker
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

    # Device list entry keys
    # device_list = {"uuid-n": {"base_device": device, "last_update": datetime}}
    BASE_DEVICE = "base_device" # As known by the Meross module
    LAST_UPDATE = "last_update" # Time of last device update
    UPDATE_LIFETIME = 60.0 * 10.0 # 10 minutes
    ASYNC_UPDATE_TIMEOUT = 5.0 # 5 seconds
    COMMAND_TIMEOUT = 5.0 # 5 seconds

    def __init__(self, name="MerossAdapterThread"):
        super().__init__(name=name)
        self._http_api_client = None
        self._rate_limiter = None
        self._manager = None

        # This dict contains all currently known devices.
        # It is keyed by device uuid.
        # Each device uuid entry contains a base_device and updated indicator.
        self._all_devices = {}

    def dispatch_request(self):
        """
        Dispatch an adapter request.
        This method is called on the new thread by the base class run method.
        The server terminates when the close request is received.
        :return: Returns the result from running the request.
        """
        result = None

        logger.debug("Dispatching Meross request %s", self._request.request)

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
            result = self._loop.run_until_complete(self.is_on(**self._request.kwargs))
        else:
            logger.error("Unrecognized request: %s", self._request.request)
            result = False

        logger.debug("Dispatched Meross request %s", self._request.request)

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
                logger.debug("Attempting %d to create a MerossHttpClient instance", retry)
                # Initiates the Meross Cloud Manager.
                # This is in charge of handling the communication with the Meross cloud (MQTT service)
                self._http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password)

                # What was learned by trial and error:
                # The design of the meross-iot module was targeted for smaller sets of devices (<10).
                # We have more than 20. The meross-iot package has gone through a number of
                # designs.

                logger.debug("Creating Meross manager instance")
                # global_burst_rate: Global burst rate, max number of commands that can be executed within the global_time_window
                # global_time_window: Time window in seconds that is used to aggregate the API counting
                # global_tokens_per_interval: Number of calls allowed within the time interval at run time (globally)
                # device_burst_rate: Per device burst rate, max number of commands that can be executed on a specific device within he device_time_window
                # device_time_window: Time window in seconds that is used to aggregate the API counting for a given device
                # device_tokens_per_interval: Number of calls allowed within the time interval at run time (per device)
                # device_max_command_queue: Maximum number of commands that can be delayed for a given device, after which commands are dropped
                self._rate_limiter = RateLimitChecker(
                    global_burst_rate=10,
                    global_time_window=timedelta(seconds=1),
                    global_tokens_per_interval=10,
                    device_burst_rate=1,
                    device_time_window=timedelta(seconds=1),
                    device_tokens_per_interval=1,
                    device_max_command_queue=5)
                self._manager = MerossManager(http_client=self._http_api_client,
                                              loop=self._loop,
                                              rate_limiter=self._rate_limiter)

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
                device_entry = self._get_device(house_device_code)
                if device_entry is None:
                    continue
                device = device_entry[MerossAdapterThread.BASE_DEVICE]
                await self._update_device(device.uuid)
                # Currently, a bulb is the only Meross device that supports color
                if self._supports_color(device):
                    await device.async_set_light_color(channel=channel,
                                                       rgb=rgb_color,
                                                       timeout=MerossAdapterThread.COMMAND_TIMEOUT)
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
                device_entry = self._get_device(house_device_code)
                if device_entry is None:
                    continue
                device = device_entry[MerossAdapterThread.BASE_DEVICE]
                await self._update_device(device.uuid)
                # Currently, a bulb is the only Meross device that supports brightness
                if self._supports_brightness(device):
                    await device.async_set_light_color(channel=channel,
                                                       luminance=brightness,
                                                       timeout=MerossAdapterThread.COMMAND_TIMEOUT)
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
                device_entry = self._get_device(house_device_code)
                if device_entry is None:
                    continue
                device = device_entry[MerossAdapterThread.BASE_DEVICE]
                await self._update_device(device.uuid)
                await device.async_turn_on(channel, timeout=MerossAdapterThread.COMMAND_TIMEOUT)
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
                device_entry = self._get_device(house_device_code)
                device = device_entry[MerossAdapterThread.BASE_DEVICE]
                if device is None:
                    continue
                await self._update_device(device.uuid)
                await device.async_turn_off(channel, timeout=MerossAdapterThread.COMMAND_TIMEOUT)
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
            for uuid, device_entry in self._all_devices.items():
                available_devices[uuid] = self._build_device_details(device_entry[MerossAdapterThread.BASE_DEVICE])
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
        try:
            await self._manager.async_device_discovery(update_subdevice_status=False)
        except Exception as ex:
            logger.error("Unhandled exception from async_device_discovery")
            logger.error(str(ex))
            return False

        logger.debug("All Meross devices discovered")

        # Find and update ALL devices
        logger.debug("Updating all discovered Meross devices")
        self._all_devices = {}
        try:
            discovered_devices = self._manager.find_devices()
            for device in discovered_devices:
                self._all_devices[device.uuid] = {
                    MerossAdapterThread.BASE_DEVICE: device,
                    MerossAdapterThread.LAST_UPDATE: None
                }
            logger.debug("All discovered Meross devices have been updated")
        except Exception as ex:
            logger.error("Unhandled exception from async_update")
            logger.error(str(ex))
            return False

        return True

    def get_device_type(self, device_address, device_channel):
        """
        Determine the type of a given device
        :param device_address:
        :param device_channel: 0-n
        :return: Either plug or bulb.
        """
        device_entry = self._get_device(device_address)
        if device_entry is None:
            return MerossAdapterThread.DEVICE_TYPE_UNKNOWN
        device = device_entry[MerossAdapterThread.BASE_DEVICE]
        if device.type.lower().startswith("msl"):
            return MerossAdapterThread.DEVICE_TYPE_BULB
        # The default
        return MerossAdapterThread.DEVICE_TYPE_PLUG

    async def is_on(self, device_address, device_channel):
        """
        Determine the on/off status of a device
        :param device_address:
        :param device_channel: 0-n
        :return: True if the device is on.
        """
        device_entry = self._get_device(device_address)
        if device_entry is None:
            return False
        device = device_entry[MerossAdapterThread.BASE_DEVICE]
        if device is not None and hasattr(device, "is_on"):
            await self._update_device(device.uuid)
            logger.debug("Calling is_on for Meross device %s", device.uuid)
            try:
                return device.is_on()
            except Exception as ex:
                logger.error("Unhandled exception from is_on %s", device_address)
                logger.error(str(ex))
        return False

    def _get_device(self, device_uuid):
        """
        Return the device instance for a given device.
        :param device_uuid: UUID of device, the key to the device list entry
        :return: Device dict entry or None
        """
        device = None

        # Look in current set of all devices first
        if device_uuid in self._all_devices:
            logger.debug("Meross device %s found in all_devices dict", device_uuid)
            return self._all_devices[device_uuid]

        logger.warning("Meross device %s was not found in all_devices dict", device_uuid)
        for retry in range(MerossAdapterThread.RETRY_COUNT):
            try:
                devices = self._manager.find_devices(device_uuids=[device_uuid])
                if devices is None:
                    continue
                if len(devices) < 1:
                    continue
                device = devices[0]
                # Add to dict of all known devices
                self._all_devices[device_uuid] = {
                    MerossAdapterThread.BASE_DEVICE: device,
                    MerossAdapterThread.LAST_UPDATE: None
                }
                return self._all_devices[device_uuid]
            except Exception as ex:
                logger.error("Exception attempting to get Meross device instance for %s", device_uuid)
                logger.error(str(ex))
                self.last_error_code = MerossAdapterThread.MEROSS_ERROR
                self.last_error = str(ex)
            finally:
                pass

        if device is None:
            logger.error("Meross device %s was not found", device_uuid)

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
        supports_color = False
        if a is not None:
            supports_color = device.get_supports_rgb()
        return supports_color


    def _supports_brightness(self, device):
        """
        Somewhat risky test to see if a device supports brightness
        :param device:
        :return:
        """
        a = getattr(device, "get_supports_luminance", None)
        supports_luminance = False
        if a is not None:
            supports_luminance = device.get_supports_luminance()
        return supports_luminance

    async def _update_device(self, device_uuid):
        """
        Optimally update the state of a device
        :param device_uuid: uuid of device to be updated
        :return: None
        """
        # An update is required if one has not been done OR the last update has expired
        update_required = self._all_devices[device_uuid][MerossAdapterThread.LAST_UPDATE] is None
        if not update_required:
            elapsed = datetime.now() - self._all_devices[device_uuid][MerossAdapterThread.LAST_UPDATE]
            update_required = elapsed.total_seconds() > MerossAdapterThread.UPDATE_LIFETIME

        success = False

        if update_required:
            for retry in range(MerossAdapterThread.RETRY_COUNT):
                logger.debug("Running async_update (retry=%d) for Meross device %s", retry + 1, device_uuid)
                try:
                    await self._all_devices[device_uuid][MerossAdapterThread.BASE_DEVICE].async_update(
                        timeout=MerossAdapterThread.ASYNC_UPDATE_TIMEOUT)
                    self._all_devices[device_uuid][MerossAdapterThread.LAST_UPDATE] = datetime.now()
                    success = True
                except CommandTimeoutError as ex:
                    logger.error("CommandTimeoutError exception during async_update")
                    logger.error(ex.message)
                    logger.error("uuid %s", ex.target_device_uuid)
                    logger.error("timeout %f", ex.timeout)
                except Exception as ex:
                    logger.error("Unhandled exception from async_update %s", device_uuid)
                    logger.error(str(ex))
                    logger.error(ex)
                if success:
                    break
        else:
            logger.debug("async_update was not required for Meross device %s", device_uuid)

        return success
