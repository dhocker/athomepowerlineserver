#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Action Factory for Timer Triggered Actions
#

import drivers.X10ControllerAdapter
from drivers.device_driver_manager import DeviceDriverManager
import logging

logger = logging.getLogger("server")


def RunAction(command, device_id, device_type, device_address, dim_amount):
    # TODO This has to be abstracted based on device type/name
    driver = DeviceDriverManager.get_driver(device_type)
    # Cases for command
    if command == "on":
        driver.DeviceOn(device_type, device_address, dim_amount)
    elif command == "off":
        driver.DeviceOff(device_type, device_address, dim_amount)
    elif command == "dim":
        driver.DeviceDim(device_type, device_address, dim_amount)
    elif (command == "bright") or (command == "brighten"):
        # The dim_amount is really a bright_amount
        driver.DeviceBright(device_type, device_address, dim_amount)
    else:
        run_all_units_action(command, device_id, device_type, device_address)


def run_all_units_action(command, device_id, device_type, device_address):
    # if command == "allunitsoff":
    #     driver.DeviceAllUnitsOff(device_type, device_address[0:1])
    # elif command == "alllightsoff":
    #     driver.DeviceAllLightsOff(device_type, device_address[0:1])
    # elif command == "alllightson":
    #     driver.DeviceAllLightsOn(device_type, device_address[0:1])
    pass