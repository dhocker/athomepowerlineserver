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
import drivers.Dummy
import drivers.XTB232

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

    @classmethod
    def init(cls, driver_list_config):
        for device_name, driver_name in driver_list_config.items():
            # X10 devices
            device_name = device_name.lower()
            driver_name = driver_name.lower()
            if device_name in cls.X10_DEVICE_LIST:
                if driver_name in cls.X10_DRIVER_LIST:
                    cls.driver_list[device_name] = drivers.XTB232.XTB232()
                elif driver_name == "dummy":
                    cls.driver_list[device_name] = drivers.Dummy.Dummy()
                else:
                    cls.driver_list[device_name] = drivers.Dummy.Dummy()

            # TODO Implement TPLink devices

    @classmethod
    def close_drivers(cls):
        # TODO Call each driver's close method
        pass

    @classmethod
    def get_driver(cls, device_name):
        if device_name in cls.driver_list.keys():
            return cls.driver_list[device_name]
        return None
