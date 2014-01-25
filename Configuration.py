#
# Server configuration
#
# The AtHomePowerlineServer.conf file holds the configuration data in JSON format.
# Currently, it looks like this:
#
# {
#   "Configuration":
#   {
#     "X10ControllerDevice": "XTB232",
#     "ComPort": "COM1"
#   }
# }
#
# The JSON parser is quite finicky about strings being quoted as shown above.
#
# This class behaves like a singleton class. There is only one instance of the configuration.
# There is no need to create an instance of this class, as everything about it is static.
#

import json
import drivers.XTB232
import drivers.Dummy

class Configuration():

  ActiveConfig = None
  
  def __init__(self):
    Configuration.LoadConfiguration()
    pass
    
  # Load the configuration file
  @classmethod
  def LoadConfiguration(cls):
    # Try to open the conf file. If there isn't one, we give up.
    try:
      cfg = open('AtHomePowerlineServer.conf', 'r')
    except Exception as ex:
      print "Unable to open AtHomePowerlineServer.conf"
      print str(ex)
      return
      
    # Read the entire contents of the conf file           
    cfg_json = cfg.read()
    cfg.close()
    #print cfg_json
    
    # Try to parse the conf file into a Python structure
    try:
      config = json.loads(cfg_json)
      # The interesting part of the configuration is in the "Configuration" section.
      cls.ActiveConfig = config["Configuration"]
    except Exception as ex:
      print "Unable to parse configuration file as JSON"
      print str(ex)
      return
      
    #print str(Configuration.ActiveConfig)
    return
    
  # Get the X10 controller device. Used to determine what driver should be used.
  @classmethod
  def X10ControllerDevice(cls):
    return cls.ActiveConfig["X10ControllerDevice"]
    
  # Get the driver instance called out by the configuration
  @classmethod
  def GetX10ControllerDriver(cls):
    dev = cls.X10ControllerDevice()
    if (dev == "XTB232") or (dev == "XTB-232"):
      return drivers.XTB232.XTB232()
    elif dev == "CM11A":
      return drivers.XTB232.XTB232()
    elif dev == "Dummy":
      return drivers.Dummy.Dummy()
    return None
    
  @classmethod
  def ComPort(cls):
    return cls.ActiveConfig["ComPort"]
    
  @classmethod
  def Port(cls):
    return cls.ActiveConfig["Port"]    