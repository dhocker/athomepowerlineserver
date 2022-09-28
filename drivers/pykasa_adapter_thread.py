#
# Kasa/TPLink adapter thread for TPLink/Kasa devices
# Based on python-kasa package: https://github.com/python-kasa/python-kasa
# © 2020, 2021  Dave Hocker
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

import logging
from kasa import SmartPlug, SmartBulb, SmartStrip, SmartLightStrip, SmartDimmer, Discover
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

    def dispatch_request(self):
        """
        Dispatch an adapter request.
        This method is called on the new thread by the base class run method.
        The server terminates when the close request is received.
        :return: Returns the result from running the request.
        """
        result = None

        # Cases for each request/command
        # Unlike the meross-iot module, none of the python-kasa methods are async
        if self._request.request == AdapterRequest.DEVICE_ON:
            result = self.device_on(**self._request.kwargs)
        elif self._request.request == AdapterRequest.DEVICE_OFF:
            result = self.device_off(**self._request.kwargs)
        elif self._request.request == AdapterRequest.SET_BRIGHTNESS:
            result = self.set_brightness(**self._request.kwargs)
        elif self._request.request == AdapterRequest.SET_COLOR:
            result = self.set_color(**self._request.kwargs)
        elif self._request.request == AdapterRequest.OPEN:
            result = self.open(**self._request.kwargs)
        elif self._request.request == AdapterRequest.CLOSE:
            result = self.close()
        elif self._request.request == AdapterRequest.GET_DEVICE_TYPE:
            result = self.get_device_type(**self._request.kwargs)
        elif self._request.request == AdapterRequest.GET_AVAILABLE_DEVICES:
            result = self.get_available_devices()
        elif self._request.request == AdapterRequest.DISCOVER_DEVICES:
            result = self.discover_devices()
        elif self._request.request == AdapterRequest.ON_OFF_STATUS:
            result = self.is_on(**self._request.kwargs)
        else:
            logger.error("Unrecognized request: %s", self._request.request)
            result = False

        return result

    def open(self, discover_target):
        """
        Open the driver. Discovers all TPlink/Kasa devices.
        :param discover_target: Broadcast address to be used for discovering devices
        :return:
        """
        # Discover all devices
        if discover_target is not None:
            self._discover_target = discover_target
        logger.debug("PyKasa discover target: %s", self._discover_target)
        self.discover_devices()
        logger.debug("PyKasa driver opened")
        return True

    def close(self):
        """
        Close the driver. Does nothing for TPLink/Kasa devices.
        :return:
        """
        # Unconditionally, the adapter thread will terminate
        self._terminate_event.set()
        logger.debug("PyKasaAdapterThread closed")
        return True

    def set_color(self, device_type, device_name_tag, house_device_code, channel, hex_color):
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
        logger.debug("set_color for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        hsv = self._hex_to_hsv(hex_color)
        dev = self._get_device(house_device_code)
        if dev is not None and dev.is_color:
            self.clear_last_error()
            for r in range(PyKasaAdapterThread.RETRY_COUNT):
                try:
                    self._loop.run_until_complete(dev.set_hsv(int(hsv[0]), int(hsv[1]), int(hsv[2])))
                    result = True
                    break
                except Exception as ex:
                    logger.error("Retry %d", r)
                    logger.error(str(ex))
                    self.last_error = str(ex)
                    self.last_error_code = 1
            del dev
        return result

    def set_brightness(self, device_type, device_name_tag, house_device_code, channel, brightness):
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
        # TODO Requires a TPLink/Kasa bulb for testing
        logger.debug("set_brightness for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        dev = self._get_device(house_device_code)
        if dev is not None and dev.is_dimmable:
            self.clear_last_error()
            for r in range(PyKasaAdapterThread.RETRY_COUNT):
                try:
                    self._loop.run_until_complete(dev.brightness(int(brightness)))
                    result = True
                    break
                except Exception as ex:
                    logger.error("Retry %d", r)
                    logger.error(str(ex))
                    self.last_error = str(ex)
                    self.last_error_code = 1
            del dev
        return result

    def device_on(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Smart device IP address
        :param channel: 0 to n
        :return:
        """
        logger.debug("DeviceOn for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        dev = self._get_device(house_device_code)
        if dev is not None:
            result = self._exec_device_function(dev.turn_on)
            self._loop.run_until_complete(dev.update())
        else:
            result = False
        return result

    def device_off(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: Smart device IP address in this case
        :param channel: 0 to n
        :return:
        """
        logger.debug("DeviceOff for: %s %s %s %s", device_type, device_name_tag, house_device_code, channel)
        dev = self._get_device(house_device_code)
        if dev is not None:
            result = self._exec_device_function(dev.turn_off)
            self._loop.run_until_complete(dev.update())
        else:
            result = False
        return result

    def get_available_devices(self):
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
            logger.error(str(ex))

        return result

    def discover_devices(self):
        """
        Discover all TPLink/Kasa devices. This is
        equivalent to rescan for all devices.
        :return:
        """
        # Discover all devices
        logger.debug("Discovering TPLink/Kasa devices")
        # The returned dict is keyed by IP address. Change to device_id.
        devices = self._loop.run_until_complete(Discover.discover(target=self._discover_target))
        self._all_devices = {}
        for ip, dev in devices.items():
            self._all_devices[dev.device_id] = dev
            self._loop.run_until_complete(dev.update())
        
        return True

    def get_device_type(self, device_address, device_channel):
        """
        Determine the type of a given device
        :param device_address:
        :param device_channel: 0-n
        :return: Either plug or bulb.
        """
        device = self._get_device(device_address)
        return self._get_device_type(device)

    def is_on(self, device_address, device_channel):
        """
        Determine the on/off status of a device
        :param device_address:
        :param device_channel: 0-n
        :return: True if the device is on.
        """
        device = self._get_device(device_address)
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
            logger.error(str(ex))

        return attrs

    def _exec_device_function(self, device_function):
        """
        Execute a device function with retries
        :param device_function: The function to be executed
        :return:
        """
        self.clear_last_error()
        result = False
        for r in range(PyKasaAdapterThread.RETRY_COUNT):
            try:
                self._loop.run_until_complete(device_function())
                result = True
                break
            except Exception as ex:
                logger.error("Retry %d", r)
                logger.error(str(ex))
                self.last_error = str(ex)
                self.last_error_code = 1

        return result

    def _create_smart_device(self, address):
        """
        Create a TPLink SmartDevice instance for the device at a
        given IP address
        :param address: The mac address (device_id) of interest
        :return:
        """
        device = None
        # Discover all devices. This will take some time...
        device = None
        devices = self._loop.run_until_complete(Discover.discover(target=self._discover_target))
        # Look for address in the discovered devices
        for ip, dev in devices.items():
            if ip == address:
                device = dev
                break

        return device

    def _get_device(self, device_address):
        """
        Get the python-kasa device instance for a given address
        :param device_address: The mac address of the device (the device_id)
        :return: A SmartDevice object, usually a SmartPlug or SmartBulb.
        """
        if device_address in self._all_devices.keys():
            device = self._all_devices[device_address]
        else:
            device = self._create_smart_device(device_address)
            self._loop.run_until_complete(device.update())
            self._all_devices[device_address] = device
        # TODO Consider aging the the data in the device object
        return device
