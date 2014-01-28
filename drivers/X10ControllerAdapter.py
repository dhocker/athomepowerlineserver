#
# Adapter pattern for the X10 controller.
#
# This class presents a consistent interface to the rest of the server application.
# The actual controller driver to be used is injected by the server start up code.
# Note that this adapter is treated as a singleton. The app only supports a singleton
# controller at a time and that controller is represented by this adapter.
# As a result, most of the methods/properties are class or static level.
#
# TODO Add methods for X10 controller access. Use the AtHomeX10 app's driver as a model
# of what methods are needed.
#

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
    print "X10ControllerAdapter has been injected with driver:", str(driver)

  #************************************************************************
  # Open the injected driver    
  @classmethod
  def Open(cls, driver):
    cls.Driver = driver
    print "X10ControllerAdapter has been injected with driver:", str(driver)
    return cls.Driver.Open()
    
  #************************************************************************
  # Close the singleton copy of the controller driver
  @classmethod
  def Close(cls):
    result = cls.Driver.Close()
    print "X10ControllerAdapter has been closed"
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
    return cls.Driver.DeviceOn(house_device_code, dim_amount)

  #************************************************************************
  # Turn a device off
  # house_device_code = Ex. 'A1'
  # dim_amount 0 <= v <= 22
  @classmethod
  def DeviceOff(cls, house_device_code, dim_amount):
    return cls.Driver.DeviceOff(house_device_code, dim_amount)
