#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014, 2020  Dave Hocker
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


def RunAction(command, device_id, device_mfg, device_name, device_address, device_channel, color, brightness):
    if command.startswith("all"):
        run_all_units_action(command, device_id, device_mfg, device_address)
    else:
        driver = DeviceDriverManager.get_driver(device_mfg)
        # Cases for command
        if command == "on":
            driver.set_brightness(device_mfg, device_name, device_address, device_channel, brightness)
            driver.set_color(device_mfg, device_name, device_address, device_channel, color)
            driver.DeviceOn(device_mfg, device_name, device_address, device_channel)
        elif command == "off":
            driver.DeviceOff(device_mfg, device_name, device_address, device_channel)
        elif command == "dim":
            driver.DeviceDim(device_mfg, device_name, device_address, device_channel)
        elif (command == "bright") or (command == "brighten"):
            # The dim_amount is really a bright_amount
            driver.DeviceBright(device_mfg, device_name, device_address, device_channel)


def run_all_units_action(command, device_id, device_type, device_address):
    # TODO This has to be abstracted based on device type/name
    # if command == "allunitsoff":
    #     driver.DeviceAllUnitsOff(device_type, device_address[0:1])
    # elif command == "alllightsoff":
    #     driver.DeviceAllLightsOff(device_type, device_address[0:1])
    # elif command == "alllightson":
    #     driver.DeviceAllLightsOn(device_type, device_address[0:1])
    pass