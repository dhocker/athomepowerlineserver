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

logger = logging.getLogger("server")

class DeviceDriverManager():
    """
    Singleton class for managing current configuration of device drivers
    """
    # device name to device driver look up table
    driver_list = {}

    # All of the supported X10 devices and drivers
    X10_DEVICE_LIST = ["x10", "x10-appliance", "x10-lamp"]
    X10_DRIVER_LIST = ["xtb232", "xtb-232", "cm11a", "cm11"]

    # All of the supported TPLink/Kasa devices and drivers
    TPLINK_DEVICE_LIST = ["tplink", "hs100", "hs103", "hs105", "hs107", "smartplug", "smartswitch", "smartbulb"]
    TPLINK_DRIVER_LIST = ["tplink"]

    # Driver list for creating a custom device name
    # DriverName:DriverClass
    DRIVER_LIST = {
        "xtb232": XTB232,
        "tplink": TPLinkDriver,
        "dummy": Dummy
    }

    @classmethod
    def init(cls, driver_list_config):
        for device_name, driver_name in driver_list_config.items():
            # X10 devices
            device_name = device_name.lower()
            driver_name = driver_name.lower()
            if device_name in cls.X10_DEVICE_LIST:
                if driver_name in cls.X10_DRIVER_LIST:
                    cls.driver_list[device_name] = XTB232()
                    logger.info("Device %s using driver %s", device_name, driver_name)
                elif driver_name == "dummy":
                    cls.driver_list[device_name] = Dummy()
                    logger.info("Device %s using driver %s", device_name, driver_name)
                else:
                    logger.error("Configuration error: unrecognized driver name %s for device %s", driver_name, device_name)
                    logger.error("Defaulting to Dummy driver for device %s", device_name)
                    cls.driver_list[device_name] = Dummy()
                    logger.info("Device %s using driver %s", device_name, driver_name)

            # TPLink/Kasa devices
            elif device_name in cls.TPLINK_DEVICE_LIST:
                if driver_name in cls.TPLINK_DRIVER_LIST:
                    cls.driver_list[device_name] = TPLinkDriver()
                    logger.info("Device %s using driver %s", device_name, driver_name)
                else:
                    logger.error("Configuration error: unrecognized driver name %s for device %s", driver_name, device_name)
                    logger.error("Defaulting to Dummy driver for device %s", device_name)
                    cls.driver_list[device_name] = Dummy()
                    logger.info("Device %s using driver %s", device_name, driver_name)

            # Custom device name
            else:
                if driver_name in cls.DRIVER_LIST.keys():
                    cls.driver_list[device_name] = cls.DRIVER_LIST[driver_name]()
                    logger.info("Custom device-to-driver mapping created: %s/%s", device_name, driver_name)
                else:
                    logger.error("Configuration error: unrecognized device name %s", device_name)
                    logger.error("Defaulting to Dummy driver for device %s", device_name)
                    cls.driver_list[device_name] = Dummy()
                    logger.info("Device %s using driver %s", device_name, driver_name)

    @classmethod
    def close_drivers(cls):
        # TODO Call each driver's close method
        pass

    @classmethod
    def get_driver(cls, device_name):
        if device_name in cls.driver_list.keys():
            return cls.driver_list[device_name]
        return None
