#
# Meross smart plug device driver research on meross-iot package
# Copyright © 2019, 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# Reference: https://github.com/albertogeniola/MerossIot
# Version 0.4.x.x of meross-iot appears to be incompatible with 0.3.4.6 - it uses asyncio
# This code uses asyncio and expects version 0.4.0.0+
#
# As a side note, it is not clear what was gained by rewriting the code to
# use asyncio. The level of complication that was introduced exceeds most of the
# gain you might get. Figuring out the request throttling scheme is a considerable
# exercise.
#

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager, RateLimitExceeded
from meross_iot.model.enums import OnlineStatus
import datetime
import asyncio
import os
from random import randint


async def meross_main(email, password):
    http_api_client = None
    manager = None

    try:
        # Initiates the Meross Cloud Manager.
        # This is in charge of handling the communication with the remote endpoint
        http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password)
        # What was learned by trial and error:
        # The design of the meross-iot module was targetted for smaller sets of devices (<10). We have approx 20.
        # burst_requests_per_second_limit default value = 1 was too small for our 19 devices.
        # over_limit_threshold_percentage default of 400.0 was too small for a large number of devices.
        manager = MerossManager(http_client=http_api_client,
                                burst_requests_per_second_limit=3, # default was 1
                                over_limit_delay_seconds=1,
                                over_limit_threshold_percentage=2000.0) # default was 400.0

        # Starts the manager
        print("async_init", datetime.datetime.now().strftime("%H:%M:%S"))
        await manager.async_init()

        # You can discover all devices or one device (by uuid)
        print("async_device_discovery all devices", datetime.datetime.now().strftime("%H:%M:%S"))
        await manager.async_device_discovery(update_subdevice_status=True)

        # You can get device access several ways
        print("find_devices for all devices", datetime.datetime.now().strftime("%H:%M:%S"))
        all_devices = manager.find_devices()

        print("All the devices found", datetime.datetime.now().strftime("%H:%M:%S"))
        active_list = []
        for p in all_devices:
            # The first time we play with a device, we must update its status
            await p.async_update()

            print("Name:", p.name, "UUID: ", p.uuid)
            # The online status is now an enum
            if not p.online_status == OnlineStatus.ONLINE:
                print("The plug %s is not online. Cannot test..." % p.name)
                continue

            # Filter out non-multi-plug devices (looking for Smart WiFi Indoor/Outdoor Plug)
            # https://www.meross.com/product/20/article/
            if p.type.lower().startswith("mss620"):
                print("Let's play with smart plug %s" % p.name)
                active_list.append(p.uuid)

                # Note that the channels property is a list of ChannelInfo objects
                print("The plug %s supports %d channels." % (p.name, len(p.channels)))

                # No longer supported
                # print("Abilities")
                # print(json.dumps(p.abilities, sort_keys=True, indent=4))

                cx = 0
                print("Turning on channel %d of %s" % (cx, p.name))
                await p.async_turn_on(cx)

                await asyncio.sleep(3)

                print("Turning off channel %d of %s" % (cx, p.name))
                await p.async_turn_off(cx)

                await asyncio.sleep(1)

            if p.type.lower().startswith("msl120"):
                print("Let's play with bulb %s" % p.name)
                active_list.append(p.uuid)

                if p.get_supports_rgb():
                    # Check the current RGB color
                    current_color = p.get_rgb_color()
                    print(f"Currently, device {p.name} is set to color (RGB) = {current_color}")
                    # Randomly chose a new color
                    rgb = randint(0, 255), randint(0, 255), randint(0, 255)
                    print(f"Chosen random color (R,G,B): {rgb}")
                    await p.async_set_light_color(rgb=rgb)
                    print("Color changed!")
                else:
                    print(f"Device {p.name} does not support color")

                if p.get_supports_luminance():
                    # Check the current luminance
                    current_luminance = p.get_luminance()
                    print(f"Currently, device {p.name} is set to luminance = {current_luminance}")
                    await p.async_set_light_color(luminance=50)
                    print("Luminance changed!")
                else:
                    print(f"Device {p.name} does not support luminance (brightness)")

        print("Testing device by UUID")
        devices_by_uuids = manager.find_devices(device_uuids=active_list)
        for device in devices_by_uuids:
            print(str(device))
            print(type(device))

            # For each channel on the device
            for cx in range(len(device.channels)):
                print("Turning on channel %d of %s" % (cx, device.name))
                await device.async_turn_on(cx)

                await asyncio.sleep(1)

                print("Turning off channel %d of %s" % (cx, device.name))
                await device.async_turn_off(cx)

                await asyncio.sleep(1)
    except RateLimitExceeded as ex:
        # Do not exit without cleaning up!
        print("RateLimitExceeded exception occurred")
    except Exception as ex:
        print("An unexpected exception occured")
        print(str(ex))

    if manager:
        print("Closing manager")
        manager.close()
    if http_api_client:
        print("Logging out of Meross cloud")
        await http_api_client.async_logout()
    print("Done")

if __name__ == '__main__':
    EMAIL = os.environ['MEROSS_EMAIL']
    PASSWORD = os.environ['MEROSS_PASSWORD']

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(meross_main(EMAIL, PASSWORD))
    # loop.close()
    asyncio.run(meross_main(EMAIL, PASSWORD))
