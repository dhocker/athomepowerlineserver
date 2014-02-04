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
# GetTime
#

import ServerCommand
import drivers.X10ControllerAdapter
import datetime

#######################################################################
# Command handler for GetTime command
# Since this is the controller, we simply return the local time
class GetTime(ServerCommand.ServerCommand):
  
  #######################################################################
  # Execute the GetTime command.
  def Execute(self, request):     
    # Generate a successful response
    response = GetTime.CreateResponse(request["request"])
    r = response["X10Response"]    

    # Success
    r['result-code'] = 0
    r['message'] = "Success"
    # Since the standard response already has a date-time value,
    # we don't have to do anything else

    return response