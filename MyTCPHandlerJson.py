#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

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
    print "Request from {}".format(self.client_address[0])
    # self.request is the TCP socket connected to the client
    self.raw_json = self.ReadJson()
    print "raw json: " + self.raw_json
    print "Request length:", len(self.raw_json)
    
    try:
      self.json = json.loads(self.raw_json)
      #print "Request: " + json.dumps(self.json)
      print "Request: " + self.json["request"]
      #print "Args: " + json.dumps(self.json["args"])

      # The command handler generates the response
      response = CommandHandler.CommandHandler().Execute(self.json)

      print "Request completed"
      
      # Return the response to the client
      self.request.sendall(json.JSONEncoder().encode(response))
    # except Exception as ex:
      # print "Exception occurred while parsing json request"
      # print str(ex)
      # print self.raw_json
      # # Send an error response???
      # raise ex
    finally:
      pass
      
    MyTCPHandlerJson.call_sequence += 1
  
  """
  Read a JSON payload from a socket
  """
  def ReadJson(self):
    depth = 0
    json_data = ""
    
    while (True):
      c = self.request.recv(1)

      if (len(json_data) == 0) and (c == "\""):
        pass
      else:
        json_data += c      
      
      if (c == "{"):
        depth += 1
      elif (c == "}"):
        depth -= 1
        if (depth == 0):
          return json_data
