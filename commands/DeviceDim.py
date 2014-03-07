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
# Device on
#

import ServerCommand
import drivers.X10ControllerAdapter
import datetime

#######################################################################
# Command handler for on command
class DeviceDim(ServerCommand.ServerCommand):
  
  #######################################################################
  # Execute the "dim" command.
  def Execute(self, request):
    """
    Executes an X10 DIM command.
    Returns true for success, false for failure.
    """
    house_device_code = request["args"]["house-device-code"]
    dim_amount = int(request["args"]["dim-amount"])

    result = drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceDim(house_device_code, dim_amount)

    # Generate a successful response
    response = DeviceDim.CreateResponse(request["request"])
    r = response["X10Response"]    
    
    r['result-code'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastErrorCode()
    if result:
      #r['error'] = "Command not fully implemented"
      r['message'] = "Success"
    else:
      r['error'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastError()
      r['message'] = "Failure"

    return response