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
# Defines the interface for a server command handler.
# All command handlers should be derived from the ServerCommand class.
#

import datetime

class ServerCommand:

  def Execute(self, request):
    response = CreateResponse()
    r = response["X10Response"]
    r['result-code'] = 404
    r['error'] = "Command not recognized"
    r['date-time'] = str(datetime.datetime.now())
    r['message'] = "none"

    return response
    
  # Create an empty response instance    
  @classmethod
  def CreateResponse(cls, command):
    response = {"X10Response": {}}
    r = response["X10Response"]    
    r['command'] = command
    r['date-time'] = str(datetime.datetime.now())
    r['server'] = "AtHomePowerlineServer"
    r['server-version'] = "1.0.0.0"
    return response