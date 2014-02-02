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

import ServerCommand
import database.Actions
import datetime

#######################################################################
# Command handler for loading actions used by timer programs
class LoadActions(ServerCommand.ServerCommand):
  
  #######################################################################
  # Execute the load actions command.
  # We replace the current set of timer programs/initiators with
  # whatever is in the request payload.
  def Execute(self, request):  
    # Reset the actions list to empty
    database.Actions.Actions.ClearActions()

    for action in request["args"]["actions"]:
      # Pull all of the timer program values out of the dict entry
      name = action["name"]
      command = action["command"]
      dim_amount = action["day-mask"]

      # Add the action to the current list
      database.Actions.Actions.AddAction(name, command, dim_amount)

    # Debugging...
    database.Actions.Actions.DumpActions()

    # Generate a successful response
    response = LoadActions.CreateResponse("LoadAction")
    r = response["X10Response"]
    
    r['result-code'] = 0
    #r['error'] = "Command not implemented"
    r['message'] = "Success"

    return response