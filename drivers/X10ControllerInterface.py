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
# Defines the interface contract for an X10 controller driver.
# Uses the abstract base class.
#

import abc
import logging

logger = logging.getLogger("server")

#######################################################################
class X10ControllerInterface:
  __metaclass__ = abc.ABCMeta

  # Error codes
  Success = 0

  #######################################################################
  def __init__(self):
    self.LastErrorCode = 0
    self.LastError = None
    logger.info("X10 controller base class initialized")
    pass
    
  #######################################################################
  @abc.abstractmethod
  def Open(self):
    pass
  
  #######################################################################  
  @abc.abstractmethod
  def Close(self):
    pass    
    
  #######################################################################
  # Return a datetime type
  @abc.abstractmethod
  def GetTime(self):
    pass        
    
  #######################################################################
  # Return controller status
  @abc.abstractmethod
  def GetStatus(self):
    pass        
    
  #######################################################################
  # TODO Consider defining this as SetCurrentTime taking no parameters.
  # Set the controller time to the current, local time.
  @abc.abstractmethod
  def SetTime(self, time_value):
    pass 

  #######################################################################
  # Reset the last error info  
  def ClearLastError(self):
    self.LastErrorCode = X10ControllerInterface.Success
    self.LastError = None

  #####################
  # X10 common methods
  #####################
  
  DeviceCodeLookup = { 1: 6, 2: 14, 3: 2, 4: 10, 5: 1, 6: 9, 7: 5, 8: 13, \
    9: 7, 10: 15, 11: 3, 12: 11, 13: 0, 14: 8, 15: 4, 16: 12 }
    
  #######################################################################
  # Return the X10 device code for a device  
  @staticmethod
  def GetDeviceCode(device_code):
    return X10ControllerInterface.DeviceCodeLookup[int(device_code)]
    
  HouseCodeLookup = { "a": 6, "b": 14, "c": 2, "d": 10, "e": 1, "f": 9, "g": 5, "h": 13, \
    "i": 7, "j": 15, "k": 3, "l": 11, "m": 0, "n": 8, "o": 4, "p": 12 }
    
  #######################################################################
  # Return the X10 house code for a house  
  # house_code is case insensitive
  @staticmethod
  def GetHouseCode(house_code):
    return X10ControllerInterface.HouseCodeLookup[house_code.lower()]
    
  #************************************************************************
  #
  # Returns day of week mask for set time
  # NOTE: This method is not required for this implementation since
  # the X10 controller does not support downloaded programs.
  #
  # Bit
  #    7  6  5  4  3  2  1  0
  #    0  Sa F  Th W  Tu M  Su
  #
  #************************************************************************
  DayOfWeekLookup = [0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x01]
  @staticmethod
  def GetDayOfWeek(dt):
    # day of week where Monday = 0 and Sunday = 7
    dow = dt.weekday()
    return X10ControllerInterface.DayOfWeekLookup[dow]
    