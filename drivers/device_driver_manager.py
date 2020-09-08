#
# AtHomePowerlineServer - networked server for various controllers
# Copyright © 2019 Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import logging
from drivers.Dummy import Dummy
from drivers.XTB232 import XTB232
from drivers.tplink import TPLinkDriver
# from drivers.py_kasa import PyKasaDriver
from drivers.meross import MerossDriver
from database.managed_devices import ManagedDevices

logger = logging.getLogger("server")

class DeviceDriverManager():
    """
    Singleton class for managing current configuration of device drivers
    """
    # device name to device driver look up table
    driver_list = {}

    # All of the supported X10 devices and drivers
    X10_DEVICE_LIST = []
    X10_DRIVER_LIST = ["xtb232", "xtb-232", "cm11a", "cm11"]

    # All of the supported TPLink/Kasa devices and drivers
    TPLINK_DEVICE_LIST = []
    TPLINK_DRIVER_LIST = ["tplink"]

    # All of the supported Meross devices and drivers
    MEROSS_DEVICE_LIST = []
    MEROSS_DRIVER_LIST = ["meross"]

    # Driver list for creating a custom device name
    # DriverName:DriverClass
    DRIVER_LIST = {
        "xtb232": XTB232,
        "tplink": TPLinkDriver,
        "meross": MerossDriver,
        "dummy": Dummy
    }

    # Tracks drivers in use. We basically treat a driver as a singleton.
    used_driver_list = {
        "xtb232": None,
        "tplink": None,
        "meross": None,
        "dummy": None
    }

    # Build list of supported devices
    # The point is to have one list of devices in the Devices model
    for device, device_mfg in ManagedDevices.VALID_DEVICE_LIST.items():
        if device_mfg == "x10":
            X10_DEVICE_LIST.append(device)
        elif device_mfg == "tplink":
            TPLINK_DEVICE_LIST.append(device)
        elif device_mfg == "meross":
            MEROSS_DEVICE_LIST.append(device)

    @classmethod
    def init(cls, driver_list_config):
        for device_name, driver_name in driver_list_config.items():
            # X10 devices
            device_name = device_name.lower()
            driver_name = driver_name.lower()
            if device_name in cls.X10_DEVICE_LIST:
                if driver_name in cls.X10_DRIVER_LIST:
                    if not cls.used_driver_list[driver_name]:
                        cls.used_driver_list[driver_name] = XTB232()
                    cls.driver_list[device_name] = cls.used_driver_list[driver_name]
                    logger.info("Device %s using driver %s", device_name, driver_name)
                elif driver_name == "dummy":
                    if not cls.used_driver_list[driver_name]:
                        cls.used_driver_list[driver_name] = Dummy()
                    cls.driver_list[device_name] = cls.used_driver_list[driver_name]
                    logger.info("Device %s using driver %s", device_name, driver_name)
                else:
                    logger.error("Configuration error: unrecognized driver name %s for device %s", driver_name, device_name)
                    logger.error("Defaulting to Dummy driver for device %s", device_name)
                    if not cls.used_driver_list[driver_name]:
                        cls.used_driver_list[driver_name] = Dummy()
                    cls.driver_list[device_name] = cls.used_driver_list[driver_name]
                    logger.info("Device %s using driver %s", device_name, driver_name)

            # TPLink/Kasa devices
            elif device_name in cls.TPLINK_DEVICE_LIST:
                if driver_name in cls.TPLINK_DRIVER_LIST:
                    if not cls.used_driver_list[driver_name]:
                        cls.used_driver_list[driver_name] = cls.DRIVER_LIST["tplink"]()
                    cls.driver_list[device_name] = cls.used_driver_list[driver_name]
                    logger.info("Device %s using driver %s", device_name, driver_name)
                else:
                    logger.error("Configuration error: unrecognized driver name %s for device %s", driver_name, device_name)
                    logger.error("Defaulting to Dummy driver for device %s", device_name)
                    if not cls.used_driver_list[driver_name]:
                        cls.used_driver_list[driver_name] = Dummy()
                    cls.driver_list[device_name] = cls.used_driver_list[driver_name]
                    logger.info("Device %s using driver %s", device_name, driver_name)

            # Meross devices
            elif device_name in cls.MEROSS_DEVICE_LIST:
                if driver_name in cls.MEROSS_DRIVER_LIST:
                    if not cls.used_driver_list[driver_name]:
                        cls.used_driver_list[driver_name] = MerossDriver()
                    cls.driver_list[device_name] = cls.used_driver_list[driver_name]
                    logger.info("Device %s using driver %s", device_name, driver_name)
                else:
                    logger.error("Configuration error: unrecognized driver name %s for device %s", driver_name, device_name)
                    logger.error("Defaulting to Dummy driver for device %s", device_name)
                    if not cls.used_driver_list[driver_name]:
                        cls.used_driver_list[driver_name] = Dummy()
                    cls.driver_list[device_name] = cls.used_driver_list[driver_name]
                    logger.info("Device %s using driver %s", device_name, driver_name)

            # Custom device name
            else:
                if driver_name in cls.DRIVER_LIST.keys():
                    # TODO This won't work if the driver is a true singleton like XTB232
                    cls.driver_list[device_name] = cls.DRIVER_LIST[driver_name]()
                    logger.info("Custom device-to-driver mapping created: %s/%s", device_name, driver_name)
                else:
                    logger.error("Configuration error: unrecognized device name %s", device_name)
                    logger.error("Defaulting to Dummy driver for device %s", device_name)
                    if not cls.used_driver_list["dummy"]:
                        cls.used_driver_list["dummy"] = Dummy()
                    cls.driver_list[device_name] = cls.used_driver_list["dummy"]
                    logger.info("Device %s using driver %s", device_name, driver_name)

        # Open all used drivers
        for dn, driver in cls.used_driver_list.items():
            if driver:
                driver.open()

    @classmethod
    def close_drivers(cls):
        # Call each driver's close method
        for dn, driver in cls.used_driver_list.items():
            if driver:
                driver.close()

    @classmethod
    def get_driver(cls, device_name):
        if device_name in cls.driver_list.keys():
            return cls.driver_list[device_name]
        return None
