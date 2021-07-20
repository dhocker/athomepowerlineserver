#
# TPLink smart plug device research
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from kasa import SmartDevice, SmartPlug, Discover
import asyncio
import logging


def enable_logging():
    # Default overrides
    logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
    logdateformat = '%Y-%m-%d %H:%M:%S'

    # Logging level override
    loglevel = logging.DEBUG

    # Configure the root logger to cover all loggers
    logger = logging.getLogger()
    logger.setLevel(loglevel)

    formatter = logging.Formatter(logformat, datefmt=logdateformat)

    # Do we log to console?
    # Covers the server and pyHS100 package
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    # logger.addHandler(ch)
    logger.addHandler(ch)


# Controlled logging shutdown
def shutdown_logging():
    logging.shutdown()
    print("Logging shutdown")


def discover_single_by_class(loop, ip):
    # plug = SmartPlug("192.168.1.181")
    plug = SmartPlug(ip)
    loop.run_until_complete(plug.update())
    print("Plug:", plug.alias)
    print(plug)

    print()
    print("Hardware")
    print(plug.hw_info)

    print()
    print("Sys Info")
    print(plug.sys_info)

    print()
    print("State:", plug.is_on)


def discover_single_by_address(loop, ip_address):
    logger = logging.getLogger()

    device = None
    try:
        device = loop.run_until_complete(Discover.discover_single(ip_address))
    except Exception as ex:
        logger.error("An exception occurred while discovering TPLink/Kasa device %s",
                     ip_address)
        logger.error(str(ex))

    if device is None:
        return

    print("Device:", device.alias)
    
    print(device)

    print()
    print("Hardware")
    print(device.hw_info)

    print()
    print("Sys Info")
    print(device.sys_info)

    print()
    print("State:", device.is_on)


def discover_devices(loop):
    # devices = loop.run_until_complete(Discover.discover(target="192.168.1.255"))
    print("Discovering devices for 5 seconds...")

    devices = loop.run_until_complete(Discover.discover(target="192.168.1.255", timeout=5, discovery_packets=3))
    for ip, device in devices.items():
        loop.run_until_complete(device.update())

    print(f"{len(devices)} devices found")
    for ip, device in devices.items():
        print(ip, "=", device.alias, type(device))


if __name__ == '__main__':
    enable_logging()

    loop = asyncio.new_event_loop()
    # discover_single_by_class(loop, "192.168.1.234")
    discover_single_by_address(loop, "192.168.1.183")
    # discover_devices(loop)
    loop.stop()
    loop.close()

    shutdown_logging()
