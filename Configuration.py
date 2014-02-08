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

########################################################################
class Configuration():

  ActiveConfig = None
  
  ######################################################################
  def __init__(self):
    Configuration.LoadConfiguration()
    pass
    
  ######################################################################
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
    
  ######################################################################
  # Get the X10 controller device. Used to determine what driver should be used.
  @classmethod
  def X10ControllerDevice(cls):
    return cls.ActiveConfig["X10ControllerDevice"]
    
  ######################################################################
  # Get the driver instance called out by the configuration
  @classmethod
  def GetX10ControllerDriver(cls):
    dev = cls.X10ControllerDevice().upper()
    if (dev == "XTB232") or (dev == "XTB-232"):
      return drivers.XTB232.XTB232()
    elif (dev == "CM11A") or (dev == "CM11"):
      return drivers.XTB232.XTB232()
    elif dev == "DUMMY":
      return drivers.Dummy.Dummy()
    return None
    
  ######################################################################
  @classmethod
  def ComPort(cls):
    return cls.ActiveConfig["ComPort"]
    
  ######################################################################
  @classmethod
  def Port(cls):
    return cls.ActiveConfig["Port"]

  ######################################################################
  @classmethod
  def Logconsole(cls):
    return cls.ActiveConfig["LogConsole"].lower() == "true"

  ######################################################################
  @classmethod
  def Logfile(cls):
    return cls.ActiveConfig["LogFile"]

  ######################################################################
  @classmethod
  def LogLevel(cls):
    return cls.ActiveConfig["LogLevel"]