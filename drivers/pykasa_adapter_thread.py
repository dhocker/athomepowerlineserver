#
# Kasa/TPLink adapter thread for TPLink/Kasa devices
# Based on python-kasa package: https://github.com/python-kasa/python-kasa
# © 2020, 2024  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# The whole point of this design is to make sure that the asyncio based code
# always runs on the same thread.
#
import asyncio
import logging
import datetime
from kasa import SmartPlug, SmartBulb, SmartStrip, SmartLightStrip, SmartDimmer, Discover
from kasa import Module
from .adapter_thread import AdapterThread
from .adapter_request import AdapterRequest

logger = logging.getLogger("server")


class PyKasaAdapterThread(AdapterThread):
    """
    Driver for TPLink/Kasa devices (SmartPlugs, SmartSwitch, SmartStrip, SmartBulb).
    Uses python-kasa package.
    """
    RETRY_COUNT = 5
    # Default discover target that limits scan to local network
    DISCOVER_TARGET = "192.168.1.255"

    def __init__(self, name="PyKasaAdapterThread"):
        """
        Initialize an instance of the python-kasa based driver
        """
        super().__init__(name=name)
        self._all_devices = None
        self._discover_target = PyKasaAdapterThread.DISCOVER_TARGET
        logger.info("PyKasa driver initialized")

    def run(self):
        """
        Run the driver in async mode
        :return: None
        """
        asyncio.run(self.async_run())

    async def async_run(self):
        """
        Run the realtime request server.
        This method is called on the new thread by the Thread class.
        The server terminates when the close request is received.
        :return: None
        """

        # Note that the close method sets the terminate event
        while not self._terminate_event.is_set():
            # This is a blocking call. The adapter thread will wait here
            # until a request arrives.
            # Termination occurs when the close() method is called and the terminate event is set.
            self._request = self._request_queue.get()
            start_time = datetime.datetime.now()

            # Cases for each request/command
            result = await self.dispatch_request()

            self._request.set_complete(result)
            elapsed_time = datetime.datetime.now() - start_time
            logger.debug("%s %s elapsed time: %f", self.adapter_name, self._request.request,
                         elapsed_time.total_seconds())

            # We are finished with this request
            self._request = None

    async def dispatch_request(self):
        """
        Dispatch an adapter request.
        This method is called on the new thread.
        The server terminates when the close request is received.
        :return: Returns the result from running the request.
        """
        result = None

        # Cases for each request/command
        # Unlike the meross-iot module, none of the python-kasa methods are async

        # TODO Make all of the requests async

        if self._request.request == AdapterRequest.DEVICE_ON:
            result = await self.device_on(**self._request.kwargs)
        elif self._request.request == AdapterRequest.DEVICE_OFF:
            result = await self.device_off(**self._request.kwargs)
        elif self._request.request == AdapterRequest.SET_BRIGHTNESS:
            result = await self.set_brightness(**self._request.kwargs)
        elif self._request.request == AdapterRequest.SET_COLOR:
            result = await self.set_color(**self._request.kwargs)
        elif self._request.request == AdapterRequest.OPEN:
            result = await self.open(**self._request.kwargs)
        elif self._request.request == AdapterRequest.CLOSE:
            result = await self.close()
        elif self._request.request == AdapterRequest.GET_DEVICE_TYPE:
            result = await self.get_device_type(**self._request.kwargs)
        elif self._request.request == AdapterRequest.GET_AVAILABLE_DEVICES:
            result = await self.get_available_devices()
        elif self._request.request == AdapterRequest.DISCOVER_DEVICES:
            result = await self.discover_devices()
        elif self._request.request == AdapterRequest.ON_OFF_STATUS:
            result = await self.is_on(**self._request.kwargs)
        else:
            logger.error("Unrecognized request: %s", self._request.request)
            result = False

        return result

    async def open(self, discover_target):
        """
        Open the driver. Discovers all TPlink/Kasa devices.
        :param discover_target: Broadcast address to be used for discovering devices
        :return:
        """
        # Discover all devices
        if discover_target is not None:
            self._discover_target = discover_target
        logger.debug("PyKasa discover target: %s", self._discover_target)
        await self.discover_devices()
        logger.debug("PyKasa driver opened")
        return True

    async def close(self):
        """
        Close the driver. Does nothing for TPLink/Kasa devices.
        :return:
        """
        # Unconditionally, the adapter thread will terminate
        self._terminate_event.set()
        logger.debug("PyKasaAdapterThread closed")
        return True

    async def set_color(self, device_type, device_name_tag, house_device_code, channel, hex_color):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Device IP address
        :param channel: 0-n
        :param hex_color: Hex color #RRGGBB
        :return: True/false
        """
        result = False

        # TODO Requires an accessible TPLink/Kasa bulb for testing
        logger.debug("set_color for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        hsv = self._hex_to_hsv(hex_color)
        dev = await self._get_device(house_device_code)
        if dev is not None:
            self.clear_last_error()
            if Module.Light in dev.modules:
                light = dev.modules[Module.Light]
                # The light must support color
                if light.is_color:
                    for r in range(PyKasaAdapterThread.RETRY_COUNT):
                        try:
                            await light.set_hsv(int(hsv[0]), int(hsv[1]), int(hsv[2]))
                            result = True
                            break
                        except Exception as ex:
                            logger.error("Retry %d", r)
                            self._log_device_exception(dev, ex)
                            self.last_error = str(ex)
                            self.last_error_code = 1
                else:
                    logger.debug("Device %s supports Light but does not support color", device_name_tag)
                    result = False
            else:
                logger.debug("Device %s does not support Light", device_name_tag)
                result = False

            del dev

        else:
            logger.error("Device %s was not found", device_name_tag)

        return result

    async def set_brightness(self, device_type, device_name_tag, house_device_code, channel, brightness):
        """
        Sets the color of the device. Ignored by devices that do not support color.
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Device address or UUID
        :param channel: 0-n
        :param brightness: 0-100 percent
        :return: True/false
        """
        result = False

        # TODO Requires an accessible TPLink/Kasa bulb for testing
        logger.debug("set_brightness for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        dev = await self._get_device(house_device_code)
        if dev is not None:
            self.clear_last_error()
            if Module.Light in dev.modules:
                light = dev.modules[Module.Light]
                for r in range(PyKasaAdapterThread.RETRY_COUNT):
                    try:
                        await light.set_brightness(brightness)
                        result = True
                        break
                    except Exception as ex:
                        logger.error("Retry %d", r)
                        self._log_device_exception(dev, ex)
                        self.last_error = str(ex)
                        self.last_error_code = 1
            else:
                logger.info("Device %s does not support Light", device_name_tag)
                result = False

            del dev

        else:
            logger.error("Device %s was not found", device_name_tag)

        return result

    async def device_on(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Smart device IP address
        :param channel: 0 to n
        :return:
        """
        logger.debug("DeviceOn for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        dev = await self._get_device(house_device_code)
        if dev is not None:
            result = await self._exec_device_function(dev, dev.turn_on)
            await dev.update()
        else:
            result = False
        return result

    async def device_off(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Smart device IP address in this case
        :param channel: 0 to n
        :return:
        """
        logger.debug("DeviceOff for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        dev = await self._get_device(house_device_code)
        if dev is not None:
            result = await self._exec_device_function(dev, dev.turn_off)
            await dev.update()
        else:
            result = False
        return result

    async def get_available_devices(self):
        """
        Get all known available TPLink/Kasa devices.
        Reference: https://github.com/GadgetReactor/pyHS100
        :return: Returns a dict where the key is the device IP address
        and the value is the human readable name of the device.
        """
        result = {}
        try:
            # Key result item by device_id instead of IP address
            for ip, dev in self._all_devices.items():
                result[dev.device_id] = self._get_device_attrs(dev)
        except Exception as ex:
            logger.error("An exception occurred while trying to enumerate available TPLink/Kasa devices")
            self._log_device_exception(dev, ex)

        return result

    async def discover_devices(self):
        """
        Discover all TPLink/Kasa devices. This is
        equivalent to rescan for all devices.
        :return:
        """
        # Discover all devices
        logger.debug("Discovering TPLink/Kasa devices")
        # The returned dict is keyed by IP address. Change to device_id.
        devices = await Discover.discover(target=self._discover_target)
        self._all_devices = {}
        for ip, dev in devices.items():
            self._all_devices[dev.device_id] = dev
            await dev.update()
        
        return True

    async def get_device_type(self, device_address, device_channel):
        """
        Determine the type of a given device
        :param device_address:
        :param device_channel: 0-n
        :return: Either plug or bulb.
        """
        device = await self._get_device(device_address)
        return self._get_device_type(device)

    async def is_on(self, device_address, device_channel):
        """
        Determine the on/off status of a device
        :param device_address:
        :param device_channel: 0-n
        :return: True if the device is on.
        """
        device = await self._get_device(device_address)
        return device.is_on

    def _get_device_type(self, dev):
        """
        Determine the type of a TPLink/Kasa device
        :param dev:
        :return:
        """
        if isinstance(dev, SmartPlug):
            device_type = PyKasaAdapterThread.DEVICE_TYPE_PLUG
        elif isinstance(dev, SmartBulb):
            device_type = PyKasaAdapterThread.DEVICE_TYPE_BULB
        elif isinstance(dev, SmartStrip):
            device_type = PyKasaAdapterThread.DEVICE_TYPE_STRIP
        elif isinstance(dev, SmartLightStrip):
            device_type = PyKasaAdapterThread.DEVICE_TYPE_LIGHTSTRIP
        elif isinstance(dev, SmartDimmer):
            device_type = PyKasaAdapterThread.DEVICE_TYPE_DIMMER
        else:
            device_type = PyKasaAdapterThread.DEVICE_TYPE_UNKNOWN

        return device_type

    def _get_device_attrs(self, dev):
        """
        Get information for a TPLink device
        :param dev:
        :return: a dict with device attributes
        """
        attrs = {}
        try:
            sys_info = dev.sys_info
            attrs["manufacturer"] = "TPLink"
            attrs["model"] = sys_info["model"]
            attrs["label"] = dev.alias
            attrs["channels"] = 1
            attrs["type"] = self._get_device_type(dev)
            # Note that this is the IP address of the device
            attrs["host"] =  dev.host
            # TODO This needs to be "by channel", but currently we only support single channel devices
            attrs["on"] = dev.is_on
            if isinstance(dev, SmartStrip) or isinstance(dev, SmartLightStrip):
                attrs["channels"] = len(sys_info["children"])
        except Exception as ex:
            logger.error("An exception occurred getting info for TPLink/Kasa device %s (%s)", dev.alias, dev.host)
            self._log_device_exception(dev, ex)

        return attrs

    async def _exec_device_function(self, dev, device_function):
        """
        Execute a device function with retries
        :param device_function: The function to be executed
        :return:
        """
        self.clear_last_error()
        result = False
        for r in range(PyKasaAdapterThread.RETRY_COUNT):
            try:
                await device_function()
                result = True
                break
            except Exception as ex:
                logger.error("Retry %d", r)
                self._log_device_exception(dev, ex)
                self.last_error = str(ex)
                self.last_error_code = 1

        return result

    async def _create_smart_device(self, address):
        """
        Create a TPLink SmartDevice instance for the device at a
        given IP address
        :param address: The mac address (device_id) of interest
        :return:
        """
        device = None
        # Discover all devices. This will take some time...
        device = None
        devices = await Discover.discover(target=self._discover_target)
        # Look for address in the discovered devices
        for ip, dev in devices.items():
            if ip == address:
                device = dev
                break

        return device

    async def _get_device(self, device_address):
        """
        Get the python-kasa device instance for a given address
        :param device_address: The mac address of the device (the device_id)
        :return: A SmartDevice object, usually a SmartPlug or SmartBulb.
        """
        if device_address in self._all_devices.keys():
            device = self._all_devices[device_address]
        else:
            device = self._create_smart_device(device_address)
            await device.update()
            self._all_devices[device_address] = device
        # TODO Consider aging the the data in the device object
        return device

    def _log_device_exception(self, dev, ex):
        """
        Log an exception on a TPLink/Kasa device including human identifiable info
        :param dev: The device object where the error occurred
        :param ex: The exception
        :return: None
        """
        logger.error(f"Exception on TPLink/Kasa device {dev.alias} at {dev.host}")
        logger.error(str(ex))
