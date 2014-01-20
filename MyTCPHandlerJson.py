import SocketServer
import json
import CommandHandler

class MyTCPHandlerJson(SocketServer.BaseRequestHandler):
  """
  The RequestHandler class for our server.

  It is instantiated once per connection to the server, and must
  override the handle() method to implement communication to the
  client.
  """
  
  call_sequence = 1

  """
  This handler uses raw data from the SocketServer.TCPServer class.
  """
  def handle(self):
    # self.request is the TCP socket connected to the client
    self.raw_json = self.ReadJson()
    print "raw json: " + self.raw_json
    self.json = json.loads(self.raw_json)
    print "{} wrote:".format(self.client_address[0])
    print "Payload: " + json.dumps(self.json)
    print "Command: " + self.json["command"]
    print "Args: " + json.dumps(self.json["args"])
    # just send back the same data, but upper-cased
    # In a real server app, we would send back a meaningful response.
    
    response = CommandHandler.CommandHandler().Execute(self.json)
    
    self.request.sendall(json.JSONEncoder().encode(response))
    
    MyTCPHandlerJson.call_sequence += 1
  
  """
  Read a JSON payload from a socket
  """
  def ReadJson(self):
    depth = 0
    json_data = ""
    
    while (True):
      c = self.request.recv(1)
      json_data += c
      
      if (c == "{"):
        depth += 1
      if (c == "}"):
        depth -= 1
        if (depth == 0):
          return json_data
