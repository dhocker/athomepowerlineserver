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

def RunAction(command, house_device_code, dim_amount):
  # Cases for command
  if command == "on":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOn(house_device_code, dim_amount)
  elif command == "off":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOff(house_device_code, dim_amount)
  elif command == "dim":
    drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceDim(house_device_code, dim_amount)
  else:
    pass
