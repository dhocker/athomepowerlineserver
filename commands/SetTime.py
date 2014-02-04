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
# SetTime
#

import ServerCommand
import drivers.X10ControllerAdapter
import datetime

#######################################################################
# Command handler for GetTime command
# We always use the host machine time. Therefor, we don't do
# anything for this command
class SetTime(ServerCommand.ServerCommand):
  
  #######################################################################
  # Execute the GetTime command.
  def Execute(self, request):     
    # Generate a successful response
    response = SetTime.CreateResponse(request["request"])
    r = response["X10Response"]    

    # Success
    r['result-code'] = 0
    r['message'] = "Success"

    return response