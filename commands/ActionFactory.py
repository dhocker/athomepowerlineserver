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
import logging

logger = logging.getLogger("server")

def RunAction(command, device_id, device_type, device_address, dim_amount):
  # TODO This has to be abstracted based on device type
  # Cases for command
  if command == "on":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOn(device_type, device_address, dim_amount)
  elif command == "off":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOff(device_type, device_address, dim_amount)
  elif command == "dim":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceDim(device_type, device_address, dim_amount)
  elif (command == "bright") or (command == "brighten"):
    # The dim_amount is really a bright_amount
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceBright(device_type, device_address, dim_amount)
  elif command == "allunitsoff":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceAllUnitsOff(device_type, device_address[0:1])
  elif command == "alllightsoff":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceAllLightsOff(device_type, device_address[0:1])
  elif command == "alllightson":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceAllLightsOn(device_type, device_address[0:1])
  else:
    pass
