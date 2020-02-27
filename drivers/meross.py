#
# Meross WiFi device driver
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# Supported devices (currently only channel 0)
#   MSS110 mini-plug https://www.meross.com/product/2/article/
#
# Untested devices that may work (on/off only)
#   MSL120 Smart WiFi LED Bulb with Color Changing (no color support)
#   MSS210 Smart WiFi Plug
#   MSS310 Smart WiFi Plug with Energy Monitor
#   MSS425E Smart WiFi Surge Protector (channel 0 only)
#
# TODO Potential design changes
#   Support multiple channel devices (e.g. multi-outlet surge protector)
#   Support color changing bulbs (e.g. MSL120)

# Reference: https://github.com/albertogeniola/MerossIot
from meross_iot.manager import MerossManager
# from meross_iot.meross_event import MerossEventType
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
import logging
import time
from .base_driver_interface import BaseDriverInterface
from Configuration import Configuration

logger = logging.getLogger("server")


class MerossDriver(BaseDriverInterface):
    MEROSS_ERROR = 7
    RETRY_COUNT = 5

    def __init__(self):
        super().__init__()
        # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint.
        # There is an inordinate amount of retry code here. But, the Meross-iot package seems
        # go through a number of network errors when the server is started as part of a fresh boot-up.
        # There's probably a race condition where the network is not completely up.
        for retry in range(1, 11):
            try:
                logger.debug("Attempt %d to create a MerossManager instance", retry)
                self._manager = MerossManager(meross_email=Configuration.MerossEmail(),
                                              meross_password=Configuration.MerossPassword())
                logger.info("Meross driver initialized")
                return
            except Exception as ex:
                logger.error("Unhandled exception attempting to create a MerossManager instance")
                logger.error("Exception type is %s", type(ex))
                # Wait incrementally longer for network to settle
                logger.debug("Waiting %d second(s) to retry", retry)
                time.sleep(float(retry))

        logger.error("After 10 retries, unable to create MerossManager instance")

    # Open the device
    def Open(self):
        # Register event handlers for the manager...(this does not appear to be required)
        # manager.register_event_handler(event_handler)
        # Starts the manager
        self.ClearLastError()
        try:
            self._manager.start()
            logger.info("Meross driver opened")
            return True
        except Exception as ex:
            logger.error("Exeception during manager.start()")
            logger.error(str(ex))
            self.LastErrorCode = MerossDriver.MEROSS_ERROR
            self.LastError = str(ex)
        return False

    # Close the device
    def Close(self):
        self.ClearLastError()
        try:
            self._manager.stop()
            logger.info("Meross driver closed")
            return True
        except Exception as ex:
            logger.error("Exeception during manager.stop()")
            logger.error(str(ex))
            self.LastErrorCode = MerossDriver.MEROSS_ERROR
            self.LastError = str(ex)
        return False

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
        try:
            device = self._get_device(house_device_code)
            # Currently, a bulb is the only Meross device that supports color
            if isinstance(device, GenericBulb):
                rgb_color = self.hex_to_rgb(hex_color)
                device.set_light_color(channel=channel, rgb=rgb_color)
            else:
               return False
            logger.debug("Setcolor for: %s (%s %s) %s", device_name_tag, house_device_code, channel, hex_color)
            return True
        except Exception as ex:
            logger.error("Exeception during SetColor for: %s (%s %s) %s", device_name_tag, house_device_code, channel, hex_color)
            logger.error(str(ex))
            self.LastErrorCode = MerossDriver.MEROSS_ERROR
            self.LastError = str(ex)
        finally:
            pass

    def DeviceOn(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device on
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: the UUID of the Meross device
        :param channel: 0-n
        :param dim_amount: a percent 0 to 100
        :return:
        """
        self.ClearLastError()
        try:
            device = self._get_device(house_device_code)
            if isinstance(device, GenericPlug):
                device.turn_on_channel(channel)
            elif isinstance(device, GenericBulb):
                device.turn_on()
            else:
                logger.error("Unrecognized Meross device type: %s (%s)", device_name_tag, house_device_code)
                self.LastErrorCode = MerossDriver.MEROSS_ERROR
                self.LastError = "Unrecognized Meross device type"
                return False
            logger.debug("DeviceOn for: %s (%s %s)", device_name_tag, house_device_code, channel)
            return True
        except Exception as ex:
            logger.error("Exeception during DeviceOn for: %s (%s %s)", device_name_tag, house_device_code, channel)
            logger.error(str(ex))
            self.LastErrorCode = MerossDriver.MEROSS_ERROR
            self.LastError = str(ex)
        finally:
            pass

        return False

    def DeviceOff(self, device_type, device_name_tag, house_device_code, channel):
        """
        Turn device off
        :param device_type: the device's type (e.g. x10, hs100, smartplug, etc.)
        :param device_name_tag: human readable name of device
        :param house_device_code: the UUID of the Meross device
        :param dim_amount: a percent 0 to 100
        :return:
        """
        self.ClearLastError()
        try:
            device = self._get_device(house_device_code)
            if isinstance(device, GenericPlug):
                device.turn_off_channel(channel)
            elif isinstance(device, GenericBulb):
                device.turn_off()
            else:
                logger.error("Unrecognized Meross device type: %s (%s %s)", device_name_tag, house_device_code, channel)
                self.LastErrorCode = MerossDriver.MEROSS_ERROR
                self.LastError = "Unrecognized Meross device type"
                return False
            logger.debug("DeviceOff for: %s (%s %s)", device_name_tag, house_device_code, channel)
            return True
        except Exception as ex:
            logger.error("Exeception during DeviceOff for: %s (%s %s)", device_name_tag, house_device_code, channel)
            logger.error(str(ex))
            self.LastErrorCode = MerossDriver.MEROSS_ERROR
            self.LastError = str(ex)
        finally:
            pass

        return False

    def DeviceDim(self, device_type, device_name_tag, house_device_code, channel, dim_amount):
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

    def DeviceBright(self, device_type, device_name_tag, house_device_code, channel, bright_amount):
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

    def GetAvailableDevices(self):
        """
        Get all known available devices for supported types.
        :return: Returns a dict where the key is the device UUID
        and the value is the human readable name of the device.
        """
        available_devices = {}
        try:
            # Update known devices. If devices are added to the Meross
            # cloud, they may not show up if the last start() was 
            # executed before the device(s) were added.
            self._manager.stop()
            self._manager.start()

            plugs = self._manager.get_devices_by_kind(GenericPlug)
            for p in plugs:
                available_devices[p.uuid] = self._build_device_details(p)

            bulbs = self._manager.get_devices_by_kind(GenericBulb)
            for b in bulbs:
                available_devices[b.uuid] = self._build_device_details(b)
        except Exception as ex:
            logger.error("Exeception enumerating available devices")
            logger.error(str(ex))
            self.LastErrorCode = 1
            self.LastError = str(ex)
        finally:
            pass

        return available_devices

    def get_device_type(self, device_address, device_channel):
        device = self._get_device(device_address)
        if isinstance(device, GenericPlug):
            return MerossDriver.DEVICE_TYPE_PLUG
        elif isinstance(device, GenericBulb):
            return MerossDriver.DEVICE_TYPE_BULB
        else:
            logger.error("Device is neither plug nor bulb. Strip?")
            logger.error(str(device))
            return MerossDriver.DEVICE_TYPE_PLUG

    #######################################################################
    # Set the controller time to the current, local time.
    def SetTime(self, time_value):
        pass

    def _get_device(self, device_uuid):
        """
        Return the device instance for a given device.
        :param device_uuid: UUID of device
        :return: Device instance or None
        """
        device = None
        for retry in range(MerossDriver.RETRY_COUNT):
            try:
                device = self._manager.get_device_by_uuid(device_uuid)
            except Exception as ex:
                logger.error("Exeception attempting to get Meross device instance for %s", device_uuid)
                logger.error(str(ex))
                self.LastErrorCode = MerossDriver.MEROSS_ERROR
                self.LastError = str(ex)
                # Restart the Meross manager
                self._manager.stop()
                self._manager.start()
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
        attrs["online"] = dd.online
        attrs["model"] = dd.type
        if isinstance(dd, GenericPlug):
            attrs["type"] = MerossDriver.DEVICE_TYPE_PLUG
            channels = len(dd.get_channels())
            attrs["channels"] = channels
            device_label = "{0} [{1} channel(s)]".format(dd.name, channels)
            attrs["label"] = device_label
            attrs["usb"] = dd.get_usb_channel_index() is not None
        elif isinstance(dd, GenericBulb):
            attrs["type"] = MerossDriver.DEVICE_TYPE_BULB
            attrs["channels"] = 1
            device_label = dd.name
            attrs["label"] = device_label
            attrs["usb"] = False
            if dd.online:
                # These attributes are only available if the device is online
                attrs["rgb"] = dd.is_rgb()
                attrs["temperature"] = dd.is_light_temperature()
                attrs["luminance"] = dd.supports_luminance()
            else:
                attrs["rgb"] = False
                attrs["temperature"] = False
                attrs["luminance"] = False
        else:
            attrs["type"] = "Unknown"
            device_label = dd.name


        return attrs


"""
if __name__ == '__main__':
    EMAIL = "athomex10@gmail.com"
    PASSWORD = "@hoMex10$$"

    def event_handler(eventobj):
        if eventobj.event_type == MerossEventType.DEVICE_ONLINE_STATUS:
            print("Device online status changed: %s went %s" % (eventobj.device.name, eventobj.status))
            pass

        elif eventobj.event_type == MerossEventType.DEVICE_SWITCH_STATUS:
            print("Switch state changed: Device %s (channel %d) went %s" % (eventobj.device.name, eventobj.channel_id,
                                                                            eventobj.switch_state))
        elif eventobj.event_type == MerossEventType.CLIENT_CONNECTION:
            print("MQTT connection state changed: client went %s" % eventobj.status)

            # TODO: Give example of reconnection?

        elif eventobj.event_type == MerossEventType.GARAGE_DOOR_STATUS:
            print("Garage door is now %s" % eventobj.door_state)

        else:
            print("Unknown event!")


    # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint
    manager = MerossManager(meross_email=EMAIL, meross_password=PASSWORD)

    # Register event handlers for the manager...
    manager.register_event_handler(event_handler)

    # Starts the manager
    manager.start()

    # You can retrieve the device you are looking for in various ways:
    # By kind
    # bulbs = manager.get_devices_by_kind(GenericBulb)
    plugs = manager.get_devices_by_kind(GenericPlug)
    # door_openers = manager.get_devices_by_kind(GenericGarageDoorOpener)
    # all_devices = manager.get_supported_devices()

    # Print some basic specs about the discovered devices
    # print("All the bulbs I found:")
    # for b in bulbs:
    #     print(b)

    print("All the plugs found:")
    for p in plugs:
        print(dir(p))
        if not p.online:
            print("The plug %s seems to be offline. Cannot test..." % p.name)
            continue

        print("Let's play with smart plug %s" % p.name)

        channels = len(p.get_channels())
        print("The plug %s supports %d channels." % (p.name, channels))

        print("Turning on channel %d of %s" % (0, p.name))
        p.turn_on_channel(0)

        time.sleep(1)

        print("Turning off channel %d of %s" % (0, p.name))
        p.turn_off_channel(0)

        time.sleep(1)

    print("Done")
"""
