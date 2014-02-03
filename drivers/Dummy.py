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

class Dummy(X10ControllerInterface.X10ControllerInterface):
  
  def __init__(self):
    X10ControllerInterface.X10ControllerInterface.__init__(self)
    logging.info("X10 Dummy class initialized")
    #print "House code for P:", Dummy.GetHouseCode("P")
    #print "Device code for 16:", Dummy.GetDeviceCode(16)
    pass
    
  # Open the device
  def Open(self):
    pass
    
  # Close the device
  def Close(self):
    pass    
    
  def SelectAddress(self, house_device_code):
    pass        
    
  # TODO Consider defining a method for each device function
  def ExecuteFunction(self, house_code, dim_amount, device_function):
    pass        
    
  # Return a datetime type
  def GetTime(self):
    pass        
    
  # TODO Consider defining this as SetCurrentTime taking no parameters.
  # Set the controller time to the current, local time.
  def SetTime(self, time_value):
    pass            