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
# Adapter pattern for the X10 controller.
#
# This class presents a consistent interface to the rest of the server application.
# The actual controller driver to be used is injected by the server start up code.
# Note that this adapter is treated as a singleton. The app only supports a singleton
# controller at a time and that controller is represented by this adapter.
# As a result, most of the methods/properties are class or static level.
#
# Add methods for X10 controller access. Use the AtHomeX10 app's driver as a model
# of what methods are needed.
#

import logging

logger = logging.getLogger("server")

class X10ControllerAdapter:
  # Injection point for driver to be used to access X10 controller
  # This is a singleton instance of the driver to be used for all access
  Driver = None
  
  #************************************************************************
  # Constructor
  def __init__(self):
    pass
   
  #************************************************************************
  # Inject driver into the adapter
  # The main app must create an instance of a driver that implements the 
  # X10ControllerInterface and call this method to inject the instance.
  @classmethod
  def InjectDriver(cls, driver):
    cls.Driver = driver
    logger.info("X10ControllerAdapter has been injected with driver: %s", str(driver))

  #************************************************************************
  # Open the injected driver    
  @classmethod
  def Open(cls, driver):
    cls.Driver = driver
    logger.info("X10ControllerAdapter has been injected with driver: %s", str(driver))
    return cls.Driver.Open()
    
  #************************************************************************
  # Close the singleton copy of the controller driver
  @classmethod
  def Close(cls):
    result = cls.Driver.Close()
    logger.info("X10ControllerAdapter has been closed")
    return result

  @classmethod
  def GetLastErrorCode(cls):
    return cls.Driver.LastErrorCode

  @classmethod
  def GetLastError(cls):
    return cls.Driver.LastError

  #************************************************************************
  # Turn a device on
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 22
  @classmethod
  def DeviceOn(cls, house_device_code, dim_amount):
    logger.info("Device on: {} {}".format(house_device_code, dim_amount))
    return cls.Driver.DeviceOn(house_device_code, dim_amount)

  #************************************************************************
  # Turn a device off
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 22
  @classmethod
  def DeviceOff(cls, house_device_code, dim_amount):
    logger.info("Device off: {} {}".format(house_device_code, dim_amount))
    return cls.Driver.DeviceOff(house_device_code, dim_amount)

  #************************************************************************
  # Dim a lamp module
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 22
  @classmethod
  def DeviceDim(cls, house_device_code, dim_amount):
    logger.info("Device dim: {0} {1}".format(house_device_code, dim_amount))
    return cls.Driver.DeviceDim(house_device_code, dim_amount)

  #************************************************************************
  # Bright(en) a lamp module
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 22
  @classmethod
  def DeviceBright(cls, house_device_code, bright_amount):
    logger.info("Device bright: {0} {1}".format(house_device_code, bright_amount))
    return cls.Driver.DeviceBright(house_device_code, bright_amount)

  #************************************************************************
  # Turn all units off
  @classmethod
  def DeviceAllUnitsOff(cls, house_code):
    logger.info("Device all units off for house code: {0}".format(house_code))
    return cls.Driver.DeviceAllUnitsOff(house_code)

  #************************************************************************
  # Turn all lights off
  @classmethod
  def DeviceAllLightsOff(cls, house_code):
    logger.info("Device all lights off")
    return cls.Driver.DeviceAllLightsOff(house_code)
