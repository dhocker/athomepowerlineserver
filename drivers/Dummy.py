#
# Dummy device driver that works for all devices
# Copyright © 2014, 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import drivers.X10ControllerInterface as X10ControllerInterface
from .base_driver_interface import BaseDriverInterface
import logging

logger = logging.getLogger("server")

class Dummy(BaseDriverInterface):
  
  def __init__(self):
    super().__init__()
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
  # Turn all lights on
  # house_code = "A"..."P"
  def DeviceAllLightsOn(self, house_code):
    logger.debug("DeviceAllLightsOn for: %s", house_code)
    return True

  #######################################################################
  # Set the controller time to the current, local time.
  def SetTime(self, time_value):
    pass
