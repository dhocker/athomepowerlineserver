#
# Adapter pattern for the X10 controller.
#
# This class presents a consistent interface to the rest of the server application.
# The actual controller driver to be used is injected by the server start up code.
#

class X10ControllerAdapter:
  # Injection point for driver to be used to access X10 controller
  Driver = None
  
  # Constructor
  def __init__(self):
    pass
   
  # Inject driver into the adapter  
  @classmethod
  def InjectDriver(self, driver):
    X10ControllerAdapter.Driver = driver
    print "X10ControllerAdapter has been injected with driver:", str(driver)
    
