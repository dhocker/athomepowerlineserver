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
    result = drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceOn(request["args"][0]["housedevicecode"], int(request["args"][0]["dimamount"]))
    
    # Generate a successful response
    response = DeviceOn.CreateResponse()
    r = response["X10Response"]    
    r['command'] = "DeviceOn"
    r['datetime'] = str(datetime.datetime.now())
    
    if result:
      r['resultcode'] = 0
      #r['error'] = "Command not fully implemented"
      r['message'] = "Success"
    else:
      r['resultcode'] = 400
      #r['error'] = "Command not fully implemented"
      r['message'] = "Failure"

      return response