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
# Timer program actions
#

import drivers.X10ControllerAdapter

########################################################################
# Action factory
def GetAction(action_name):
  ci_command = action_name.lower()

  if ci_command == "on":
    action = On
  elif ci_command == "off":
    action = Off
  elif ci_command == "dim":
    action = Dim
  else:
    action = None

  return action

########################################################################
# Device/light on
def On(house_device_code, dim_amount, args):
  drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOn(house_device_code, dim_amount)

########################################################################
# Device/light off
def Off(house_device_code, dim_amount, args):
  drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOff(house_device_code, dim_amount)

########################################################################
# Lamp module dim
def Dim(house_device_code, dim_amount, args):
  drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceDim(house_device_code, dim_amount)
