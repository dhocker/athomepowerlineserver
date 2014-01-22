import ServerCommand
import datetime
#import drivers.X10ControllerAdapter

# Command handler for controller status request
class StatusRequest(ServerCommand.ServerCommand):
  
  # Execute the status request command.
  # You might think we have to call the controller to get its
  # status, but it is not clear that is necessary.
  def Execute(self, request):
      response = StatusRequest.CreateResponse()
      r = response["X10Response"]
      
      tod = datetime.datetime.now()
      
      r['command'] = "StatusRequest"
      r['resultcode'] = 0
      #r['error'] = "Command not implemented"
      r['datetime'] = str(tod)
      # day of week: 0=Monday, 6=Sunday. This is different from the CM11a spec.
      r['dayofweek'] = str(tod.weekday())
      r['firmwarerevision'] = '0.0.0.0'
      r['message'] = "Success"

      return response