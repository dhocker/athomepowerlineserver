import json
import datetime
import commands.ServerCommand
import commands.LoadTimers
import commands.ServerCommand
import commands.StatusRequest
import commands.DeviceOn

class CommandHandler:
  
  call_sequence = 1
  
  # Return an instance of the handler for a given command
  #
  # Complete list of CM11A functions from protocol spec
  # Function			            Binary Value
	# All Units Off			        0000
	# All Lights On			        0001
	# On				                0010
	# Off				                0011
	# Dim				                0100
	# Bright				            0101
	# All Lights Off		        0110
	# Extended Code			        0111
	# Hail Request			        1000
	# Hail Acknowledge	        1001
	# Pre-set Dim (1)		        1010
	# Pre-set Dim (2)		        1011
	# Extended Data Transfer		1100
	# Status On			            1101	
	# Status Off			          1110
	# Status Request		        1111
  def GetHandler(self, command):
    print "GetHandler for command:", command
    
    ci_command = command.lower()
    
    if ci_command == "loadtimers":
      handler = commands.LoadTimers.LoadTimers()
    elif ci_command == "deviceon":
      handler = commands.DeviceOn.DeviceOn()
    elif ci_command == "deviceoff":
      handler = None
    elif ci_command == "allunitsoff":
      handler = None
    elif ci_command == "alllightson":
      handler = None
    elif ci_command == "dim":
      handler = None
    elif ci_command == "bright":
      handler = None
    elif ci_command == "alllightsoff":
      handler = None
    elif ci_command == "statusrequest":
      handler = commands.StatusRequest.StatusRequest()
    elif ci_command == "currentime":
      handler = None
    elif ci_command == "settime":
      handler = None
    else:
      handler = None
      
    return handler  

  # Execute the command specified by the incoming request
  def Execute(self, request):
    handler = self.GetHandler(request["command"])
    if handler is not None:
      response = handler.Execute(request)
      response['X10Response']['callsequence'] = CommandHandler.call_sequence
    else:
      print "No handler for command:", request["command"]
      response = commands.ServerCommand.ServerCommand.CreateResponse(request["command"])
      r = response['X10Response']
      r['resultcode'] = 404
      r['error'] = "Command is not recognized or implemented"
      r['callsequence'] = CommandHandler.call_sequence
      r['data'] = ""
      
    CommandHandler.call_sequence += 1
    
    return response