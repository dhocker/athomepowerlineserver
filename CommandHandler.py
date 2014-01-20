import json
import datetime
import commands.LoadTimers
import commands.ServerCommand

class CommandHandler:
  
  call_sequence = 1
  
  # Return an instance of the handler for a given command
  def GetHandler(self, command):
    print "GetHandler for command:", command
    
    ci_command = command.lower()
    
    if ci_command == "loadtimers":
      handler = commands.LoadTimers.LoadTimers()
    elif ci_command == "on":
      handler = None
    elif ci_command == "off":
      handler = None
    else:
      handler = None
      
    return handler  

  def Execute(self, request):
    handler = self.GetHandler(request["command"])
    if handler is not None:
      r = handler.Execute(request)
      r['X10Response']['server'] = "AtHomePowerlineServer"
      r['X10Response']['serverversion'] = "1.0.0.0"
      r['X10Response']['callsequence'] = CommandHandler.call_sequence
      r['X10Response']['datetime'] = str(datetime.datetime.now())
    else:
      r = ServerCommand.CreateResponse()
      r['X10Response']['server'] = "AtHomePowerlineServer"
      r['X10Response']['serverversion'] = "1.0.0.0"
      r['X10Response']['resultcode'] = 404
      r['X10Response']['error'] = "Command not recognized"
      r['X10Response']['callsequence'] = CommandHandler.call_sequence
      r['X10Response']['datetime'] = str(datetime.datetime.now())
      r['X10Response']['data'] = "none"
    
    return r