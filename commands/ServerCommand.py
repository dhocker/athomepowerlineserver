import datetime

class ServerCommand:

  def Execute(self, request):
    r = CreateResponse()
    r['X10Response']['resultcode'] = 404
    r['X10Response']['error'] = "Command not recognized"
    r['X10Response']['datetime'] = str(datetime.datetime.now())
    r['X10Response']['data'] = "none"

    return r
    
# Create an empty response instance    
def CreateResponse():
  r = {"X10Response": {}}
  return r