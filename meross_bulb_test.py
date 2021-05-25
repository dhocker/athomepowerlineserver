#
# Meross bulb device driver testing
# Copyright © 2019, 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# Requires meross-iot version 0.3.4.6. Will not work with version 4+.
#

from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
# from meross_iot.cloud.devices.door_openers import GenericGarageDoorOpener
# from random import randint
import time
import os


if __name__ == '__main__':
    EMAIL = os.environ['MEROSS_EMAIL']
    PASSWORD = os.environ['MEROSS_PASSWORD']

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
    manager = MerossManager.from_email_and_password(meross_email=EMAIL, meross_password=PASSWORD)

    # Register event handlers for the manager...(this does not appear to be required)
    # manager.register_event_handler(event_handler)

    # Starts the manager
    manager.start()
    manager.stop()
    manager.start()

    # You can retrieve the device you are looking for in various ways:
    # By kind
    bulbs = manager.get_devices_by_kind(GenericBulb)
    plugs = manager.get_devices_by_kind(GenericPlug)
    # door_openers = manager.get_devices_by_kind(GenericGarageDoorOpener)
    # all_devices = manager.get_supported_devices()

    # Print some basic specs about the discovered devices
    print("All the bulbs I found:")
    for b in bulbs:
        print(b)

    # You can also retrieve devices by the UUID/name
    # a_device = manager.get_device_by_name("Meross Plug 4")
    # a_device = manager.get_device_by_uuid("1907224198291625185048e1e901d51a")
    # Or you can retrieve all the device by the HW type
    # all_mss310 = manager.get_devices_by_type("mss310")

    print("All the bulbs found:")
    active_list = []
    for b in bulbs:
        print("Name:", b.name, "UUID: ", b.uuid)
        if not b.online:
            print("The plug %s seems to be offline. Cannot test..." % b.name)
            continue

        print("Let's play with smart plug %s" % b.name)
        active_list.append(b.uuid)

    print("Testing device by UUID")
    for u in active_list:
        device = manager.get_device_by_uuid(u)
        print(str(device))

        print("Turning on channel %d of %s" % (0, device.name))
        device.turn_on_channel(0)

        time.sleep(1)

        print("Turning off channel %d of %s" % (0, device.name))
        device.turn_off_channel(0)

        time.sleep(1)
    for p in plugs:
        print("Name:", p.name, "UUID: ", p.uuid)
        print(p)
        if not p.online:
            print("The plug %s seems to be offline. Cannot test..." % p.name)
            continue

        print("Let's play with smart plug %s" % p.name)
        active_list.append(p.uuid)

        channels = len(p.get_channels())
        print("The plug %s supports %d channels." % (p.name, channels))

    manager.stop()
    print("Done")
