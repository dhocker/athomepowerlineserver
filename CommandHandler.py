import json
import datetime
import commands.LoadTimers
import commands.ServerCommand
import commands.StatusRequest

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
    elif ci_command == "on":
      handler = None
    elif ci_command == "off":
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
    else:
      handler = None
      
    return handler  

  # Execute the command specified by the incoming request
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
      r['X10Response']['error'] = "Command is not recognized or implemented"
      r['X10Response']['callsequence'] = CommandHandler.call_sequence
      r['X10Response']['datetime'] = str(datetime.datetime.now())
      r['X10Response']['data'] = "none"
      
    CommandHandler.call_sequence += 1
    
    return r