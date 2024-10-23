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
from drivers.py_kasa import PyKasaDriver
from drivers.meross_v4 import MerossDriverV4
from Configuration import Configuration

logger = logging.getLogger("server")


class DeviceDriverManager:
    """
    Singleton class for managing current configuration of device drivers
    """
    # device name to device driver look up table
    driver_list = {}

    # Driver list mapping all driver names to driver class
    DRIVER_LIST = {
        "tplink": PyKasaDriver,
        "meross": MerossDriverV4,
        "dummy": Dummy
    }

    @classmethod
    def init(cls):
        # Create driver instances for all supported manufacturers
        # Note that only one instance of each driver is created making
        # each driver a singleton.

        enabled_drivers = Configuration.enabled_drivers()

        if enabled_drivers is None or len(enabled_drivers) == 0:
            # Default to all known devices
            enabled_drivers = cls.DRIVER_LIST.keys()
            logger.debug("Configuration file does not define enabled drivers")
            logger.debug("Defaulting to all known drivers")

        for name in enabled_drivers:
            if name in cls.DRIVER_LIST.keys():
                # Create an instance of the driver
                cls.driver_list[name] = cls.DRIVER_LIST[name]()
                logger.info("Created driver for %s", name)
            else:
                logger.error("%s is not a recognized driver", name)

        # Open all used drivers
        for dn, driver in cls.driver_list.items():
            if driver is not None:
                driver.open()

        logger.debug("Driver instances created for all enabled drivers")

    @classmethod
    def close_drivers(cls):
        # Call each driver's close method
        for dn, driver in cls.driver_list.items():
            if driver:
                logger.debug("Closing driver %s", dn)
                driver.close()

    @classmethod
    def get_driver(cls, device_name):
        if device_name in cls.driver_list.keys():
            return cls.driver_list[device_name]
        return None

    @classmethod
    def discover_devices(cls):
        for device_name, driver in cls.driver_list.items():
            driver.discover_devices()
