#
# Device on
#

import ServerCommand
import drivers.X10ControllerAdapter
import datetime

# Command handler for on command
class DeviceOn(ServerCommand.ServerCommand):
  
  # Execute the "on" command.
  def Execute(self, request):     
    result = drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOn(request["args"]["housedevicecode"], int(request["args"]["dimamount"]))
    
    # Generate a successful response
    response = DeviceOn.CreateResponse("DeviceOn")
    r = response["X10Response"]    
    
    r['resultcode'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastErrorCode()
    if result:
      #r['error'] = "Command not fully implemented"
      r['message'] = "Success"
    else:
      r['error'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastError()
      r['message'] = "Failure"

      return response