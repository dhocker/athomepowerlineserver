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
# Device all lights on
#

import commands.ServerCommand as ServerCommand
import drivers.X10ControllerAdapter

#######################################################################
# Command handler for bright command
class DeviceAllLightsOn(ServerCommand.ServerCommand):

  #######################################################################
  # Execute the "on" command.
  def Execute(self, request):
    result = drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceAllLightsOn(request["args"]["house-code"])

    # Generate a successful response
    response = DeviceAllLightsOn.CreateResponse(request["request"])
    r = response["X10Response"]

    r['result-code'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastErrorCode()
    if result:
      r['message'] = "Success"
    else:
      r['error'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastError()
      r['message'] = "Failure"

    return response