#
# TPLink/Kasa diagnostic test tool
# Copyright © 2023  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# The primary objective of this diagnostic is to identify TPLink/Kasa devices
# that are not responding and need a power-off-on reset.
#
# To run:
#   workon your-venv
#   python tplink_diag.py
#


from kasa import SmartDevice, SmartPlug, Discover
import asyncio
import logging
from database.managed_devices import ManagedDevices
from Configuration import Configuration


version = "1.0.0"
logger = None


def enable_logging():
    # Default overrides
    logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
    logdateformat = '%Y-%m-%d %H:%M:%S'

    # Logging level override (only DEBUG or INFO is supported)
    log_cfg = Configuration.LogLevel().upper()
    if log_cfg == "INFO":
        loglevel = logging.INFO
    else:
        loglevel = logging.DEBUG

    # Configure the root logger to cover all loggers
    logger = logging.getLogger()
    logger.setLevel(loglevel)

    formatter = logging.Formatter(logformat, datefmt=logdateformat)

    # log to console?
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
    """
    Discover all TPLink/Kasa devices in the local network
    :param loop: An async loop instance to run the discovery on
    :return: A list of discovered TPLink device objects
    """
    logger.info("Discovering devices for 5 seconds...")

    devices = loop.run_until_complete(Discover.discover(target="192.168.1.255", timeout=5, discovery_packets=3))
    for ip, device in devices.items():
        loop.run_until_complete(device.update())

    return devices


def get_tplink_devices():
    """
    Query the AHPS ManagedDevices table for all TPLink devices
    :return: A list of ManagedDevices records where the record is a dict
    """
    md = ManagedDevices()
    managed_devices = md.get_devices_for_mfg("tplink")
    return managed_devices


def main():
    """
    Run diagnostics
    :return: None
    """
    # Query DB for all tplink devices defined in AHPS
    managed_devices = get_tplink_devices()

    # Make a dict of the devices keyed by the mac/address
    managed_macs = {}
    for i in range(len(managed_devices)):
        managed_macs[managed_devices[i]["address"]] = managed_devices[i]

    loop = asyncio.new_event_loop()

    # Discover all online TPLink/Kasa devices
    discovered_devices = discover_devices(loop)

    # Dump devices that were actually found
    logger.info(f"{len(discovered_devices)} devices were discovered")
    discovered_macs = {}
    for ip, discovered_device in discovered_devices.items():
        logger.info(f"{ip} = <{discovered_device.mac}> <{discovered_device.alias}> {type(discovered_device)}")
        discovered_macs[discovered_device.mac] = discovered_device

    # Verify that each managed device was found online
    logger.info(f"Checking {len(managed_devices)} managed devices")
    not_found = 0
    for mac, managed_device in managed_macs.items():
        if mac not in discovered_macs.keys():
            logger.error(f"***Managed device was not discovered: {mac} {managed_device['location']} {managed_device['name']}")
            not_found += 1
        else:
            dd = discovered_macs[mac]
            logger.info(f"{dd.host} = <{mac}> <{managed_device['location']}> <{managed_device['name']}>")
    if not_found > 0:
        logger.error(f"{not_found} managed device(s) were not discovered")
    else:
        logger.info("All managed devices were discovered")

    logger.info("Checking for unmanaged devices")
    not_found = 0
    for ip, device in discovered_devices.items():
        if device.mac not in managed_macs.keys():
            logger.error(f"Discovered device is not managed: {ip} {device.mac} {device.alias}")
            not_found += 1
        else:
            pass
    if not_found > 0:
        logger.error(f"{not_found} discovered device(s) are not managed")
    else:
        logger.info("All discovered devices are managed")

    loop.stop()
    loop.close()


if __name__ == '__main__':
    print("")
    print(f"TPLink/Kasa Device Diagnostic Tool {version}")
    print("")

    Configuration.load_configuration()

    enable_logging()
    logger = logging.getLogger("server")
    logger.info(f"TPLink/Kasa Device Diagnostic Tool {version}")

    main()

    shutdown_logging()
