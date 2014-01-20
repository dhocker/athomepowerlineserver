import ServerCommand
import datetime

# Command handler for loading timer initiators
class LoadTimers(ServerCommand.ServerCommand):
  
  def Execute(self, request):
      r = ServerCommand.CreateResponse()
      r['X10Response']['resultcode'] = 404
      r['X10Response']['error'] = "Command not implemented"
      r['X10Response']['datetime'] = str(datetime.datetime.now())
      r['X10Response']['data'] = "none"

      return r