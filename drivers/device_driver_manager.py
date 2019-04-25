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

    @classmethod
    def init(cls, driver_list_config):
        for device_name, driver_name in driver_list_config.items():
            if device_name.lower() in ["x10", "x10-appliance", "x10-lamp"]:
                if driver_name.lower() in ["xtb232", "xtb-232", "cm11a", "cm11"]:
                    cls.driver_list[device_name] = drivers.XTB232.XTB232()
                elif driver_name.lower() == "dummy":
                    cls.driver_list[device_name] = drivers.Dummy.Dummy()
                else:
                    cls.driver_list[device_name] = drivers.Dummy.Dummy()
            # TODO Implement TPLink devices

    @classmethod
    def get_driver(cls, device_name):
        if device_name in cls.driver_list.keys():
            return cls.driver_list[device_name]
        return None