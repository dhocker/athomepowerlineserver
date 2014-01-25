#
# Defines the interface for a server command handler.
# All command handlers should be derived from the ServerCommand class.
#

import datetime

class ServerCommand:

  def Execute(self, request):
    response = CreateResponse()
    r = response["X10Response"]
    r['resultcode'] = 404
    r['error'] = "Command not recognized"
    r['datetime'] = str(datetime.datetime.now())
    r['message'] = "none"

    return response
    
  # Create an empty response instance    
  @classmethod
  def CreateResponse(cls):
    response = {"X10Response": {}}
    return response