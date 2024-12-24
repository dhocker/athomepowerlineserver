#
# TPLink/Kasa diagnostic test tool
# Copyright © 2023, 2024  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import asyncio
from kasa import Discover, Module

async def main():
    dev = await Discover.discover_single("192.168.1.238")
    await dev.turn_on()
    await dev.update()
    print(dev.host)
    print("Modules...")
    for m in dev.modules:
        print(m)
    print("End of modules")


    if Module.Light in dev.modules:
        print("Device supports Light")
        light = dev.modules[Module.Light]
        b = light.brightness
        print(b)
        await light.set_brightness(b)
        print("Brightness set")

        if light.is_color:
            print("Device supports color")
            light.set_hsv(0, 100, 50)
        else:
            print("Device does not support color")
    else:
        print("Device does not support Light")


if __name__ == "__main__":
    asyncio.run(main())
