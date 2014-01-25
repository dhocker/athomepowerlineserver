#
# Dummy X10 controller driver
#

import X10ControllerInterface

class Dummy(X10ControllerInterface.X10ControllerInterface):
  
  def __init__(self):
    X10ControllerInterface.X10ControllerInterface.__init__(self)
    print "X10 Dummy class initialized"
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