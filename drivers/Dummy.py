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
# Dummy X10 controller driver
#

import X10ControllerInterface
import logging

logger = logging.getLogger("server")

class Dummy(X10ControllerInterface.X10ControllerInterface):
  
  def __init__(self):
    X10ControllerInterface.X10ControllerInterface.__init__(self)
    logger.info("Dummy driver initialized")
    pass
    
  # Open the device
  def Open(self):
    logger.debug("Driver opened")
    
  # Close the device
  def Close(self):
    logger.debug("Driver closed")

  #######################################################################
  # Turn a device on
  # house_device_code = Ex. 'A1'
  # dim_amount as a percent 0 <= v <= 100
  def DeviceOn(self, house_device_code, dim_amount):
    logger.debug("DeviceOn for: %s %s", house_device_code, dim_amount)
    return True

  #######################################################################
  # Turn a device off
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 100
  def DeviceOff(self, house_device_code, dim_amount):
    logger.debug("DeviceOff for: %s %s", house_device_code, dim_amount)
    return True

  #######################################################################
  # Dim a lamp module
  # house_device_code = Ex. 'A1'
  # dim_amount as a percent 0 <= v <= 100
  def DeviceDim(self, house_device_code, dim_amount):
    logger.debug("DeviceDim for: %s %s", house_device_code, dim_amount)
    return True

  #######################################################################
  # Bright(en) a lamp module
  # house_device_code = Ex. 'A1'
  # bright_amount as a percent 0 <= v <= 100
  def DeviceBright(self, house_device_code, bright_amount):
    logger.debug("DeviceBright for: %s %s", house_device_code, bright_amount)
    return True

  #######################################################################
  # Turn all units off (for a given house code)
  # house_code = "A"..."P"
  def DeviceAllUnitsOff(self, house_code):
    logger.debug("DeviceAllUnitsOff for: %s", house_code)
    return True

  #######################################################################
  # Turn all lights off
  # house_code = "A"..."P"
  def DeviceAllLightsOff(self, house_code):
    logger.debug("DeviceAllLightsOff for: %s", house_code)
    return True

  #######################################################################
  # Return a datetime type
  def GetTime(self):
    pass

  #######################################################################
  # Return controller status
  def GetStatus(self):
    pass

  #######################################################################
  # Set the controller time to the current, local time.
  def SetTime(self, time_value):
    pass

  def SelectAddress(self, house_device_code):
    pass        
    
  # TODO Consider defining a method for each device function
  def ExecuteFunction(self, house_code, dim_amount, device_function):
    pass        
