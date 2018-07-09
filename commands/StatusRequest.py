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

import commands.ServerCommand as ServerCommand
import datetime
#import drivers.X10ControllerAdapter

# Command handler for controller status request
class StatusRequest(ServerCommand.ServerCommand):
  
  # Execute the status request command.
  # You might think we have to call the controller to get its
  # status, but it is not clear that is necessary.
  def Execute(self, request):
      response = StatusRequest.CreateResponse("StatusRequest")
      r = response["X10Response"]
      
      tod = datetime.datetime.now()
      
      r['result-code'] = 0
      #r['error'] = "Command not implemented"
      # day of week: 0=Monday, 6=Sunday. This is different from the CM11a spec.
      r['day-of-week'] = str(tod.weekday())
      r['firmware-revision'] = '0.0.0.0'
      r['message'] = "Success"

      return response