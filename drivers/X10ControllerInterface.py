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
  # Turn a device on
  # house_device_code = Ex. 'A1'
  # dim_amount as a percent 0 <= v <= 100
  @abc.abstractmethod
  def DeviceOn(self, house_device_code, dim_amount):
    pass

  #######################################################################
  # Turn a device off
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 100
  @abc.abstractmethod
  def DeviceOff(self, house_device_code, dim_amount):
    pass

  #######################################################################
  # Dim a lamp module
  # house_device_code = Ex. 'A1'
  # dim_amount as a percent 0 <= v <= 100
  @abc.abstractmethod
  def DeviceDim(self, house_device_code, dim_amount):
    pass

  #######################################################################
  # Bright(en) a lamp module
  # house_device_code = Ex. 'A1'
  # bright_amount as a percent 0 <= v <= 100
  @abc.abstractmethod
  def DeviceBright(self, house_device_code, dim_amount):
    pass

  #######################################################################
  # Turn all units off (for a given house code)
  # house_code = "A"..."P"
  @abc.abstractmethod
  def DeviceAllUnitsOff(self, house_code):
    pass

  #######################################################################
  # Turn all lights off
  # house_code = "A"..."P"
  @abc.abstractmethod
  def DeviceAllLightsOff(self, house_code):
    pass

  #######################################################################
  # Turn all lights on
  # house_code = "A"..."P"
  @abc.abstractmethod
  def DeviceAllLightsOn(self, house_code):
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

  FUNCTION_LOOKUP = {0: "All Units Off",
                     1: "All Lights On",
                     2: "On",
                     3: "Off",
                     4: "Dim",
                     5: "Bright",
                     6: "All Lights Off",
                     7: "Extended Code",
                     8: "Hail Request",
                     9: "Hail Acknowledge",
                     10: "Pre-set Dim 1",
                     11: "Pre-set Dim 2",
                     12: "Extended Data Transfer",
                     13: "Status On",
                     14: "Status Off",
                     15: "Status Request"}

  @staticmethod
  def GetFunctionName(func_code):
    """
    Return the function name for a given X10 function code
    """
    return X10ControllerInterface.FUNCTION_LOOKUP[func_code]
  
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

  @staticmethod
  def GetKeyForValue(dict, find_value):
    """
    Return the dict key for a given value (reverse lookup)
    """
    for key, value in dict.items():
      if value == find_value:
        return key
    return None

  @staticmethod
  def FormatStandardTransmission(hc):
    """
    Format a two-byte header:code into human readable text.
    Useful for logging commands sent to controller.
    """
    # Bit:	      7   6   5   4   3   2   1   0
    # Header:	    < Dim amount    >   1  F/A E/S
    dim_amount = (hc[0] >> 3) & 0x1F
    sync_bit = (hc[0] & 0x04) >> 2
    f_a_bit = (hc[0] & 0x02) >> 1
    f_a_text = "F" if f_a_bit else "A"
    e_s_bit = hc[0] & 0x01
    e_s_text = "E" if e_s_bit else "S"

    line_1 = "Dim={0} Sync={1} F/A={2} E/S={3}".format(dim_amount, sync_bit, f_a_text, e_s_text)

    # Bit: 	    7   6   5   4   3   2   1   0
    # Address:  < Housecode >   <Device Code>
    # Function: < Housecode >   < Function  >
    house_code_encoded = (hc[1] >> 4) &0x0F
    house_code = X10ControllerInterface.GetKeyForValue(X10ControllerInterface.HouseCodeLookup, house_code_encoded)
    if f_a_bit:
      # Function
      func = hc[1] & 0x0F
      func_name = X10ControllerInterface.FUNCTION_LOOKUP[func]
      line_2 = "HouseCode={0} Function={1}".format(house_code, func_name)
    else:
      # Address
      device_code_encoded = hc[1] & 0x0F
      device_code = X10ControllerInterface.GetKeyForValue(X10ControllerInterface.DeviceCodeLookup, device_code_encoded)
      line_2 = "HouseCode={0} DeviceCode={1}".format(house_code.upper(), device_code)

    return line_1 + " " + line_2