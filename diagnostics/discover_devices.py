#
# TPLink/Kasa diagnostic tool to discover all devoices
# Copyright © 2023, 2024  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import asyncio
import time
import threading
from kasa import Discover


class DiscoverThread(threading.Thread):
    def __init__(self):
        super().__init__(name="python-kasa-thread")
        self.devices = None

    def run(self):
        # asyncio.run(self.main())
        asyncio.run(self._discover())

    async def _discover(self):
        print(f"Starting discovery at {time.strftime('%X')} on {self.name}")
        self.devices = await Discover.discover(
            target="192.168.1.255",
            timeout=5,
            on_discovered=None,
            on_unsupported=None,
            credentials=None,
            discovery_packets=3,
        )

        print(f"Discovery completed at {time.strftime('%X')}")

    async def say_after(self, delay, what):
        await asyncio.sleep(delay)
        print(what)

    async def main(self):
        print(f"started at {time.strftime('%X')}")

        await self.say_after(1, 'hello')
        await self.say_after(2, 'world')

        print(f"finished at {time.strftime('%X')}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # asyncio.run(main())
    print("Starting discovery thread")
    discover_thread = DiscoverThread()
    discover_thread.start()
    print("Waiting for discovery thread to end...")
    discover_thread.join()
    # use discover_thread.is_alive() to determine if thread is still running
    print(f"Discovery returned {len(discover_thread.devices)} devices")
    
    for k, v in discover_thread.devices.items():
        print(f"{k}, {type(v)} {v}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
