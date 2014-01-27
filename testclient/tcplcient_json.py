#
# Test client for AtHomeServer
#

import socket
import sys
import json
from optparse import OptionParser

#Host, Port = "localHost", 9999
Host, Port = "hedwig", 9999
#Host, Port = "192.168.1.111", 9999


# tcpclient
# Sends and receives JSON formatted payloads

# Create an empty server request
# This is the safe way to create an empty request.
# The json module seems to be a bit finicky about the
# format of strings that it converts.
def CreateRequest(command):
  request = {}
  request["command"] = command
  # The args parameter is an array. For commands like load timer programs,
  # each array element is a dict that defines a timer program. For commands
  # that  have a single arg, there is only a single array element.
  request["args"] = []
  return request

# Open a socket to the server 
# Note that a socket can only be used for one request.
# The server seems to close the socket at when it is
# finished handling the request. 
def ConnectToServer(Host):
  
  # Create a socket (SOCK_STREAM means a TCP socket)
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    # Connect to server and check status
    sock.connect((Host, Port))
    return sock
  except Exception as ex:
    print "Unable to connect to server:", Host, Port
    print str(ex)
  
  return None
  
# Read a JSON payload from a socket
def ReadJson(sock):
  depth = 0
  json_data = ""
  
  while (True):
    c = sock.recv(1)
    json_data += c
    
    if (c == "{"):
      depth += 1
    if (c == "}"):
      depth -= 1
      if (depth == 0):
        return json_data

# Display a formatted response on the console        
def DisplayResponse(response):
    jr = json.loads(response)["X10Response"]
    
    print "Response for command:", jr["command"]
   
    # Loop through all of the entries in the response dict
    for k, v in jr.iteritems():
      if k != "command":
        print " ", k, ":", v
        
# Test the Device On command        
def DeviceOn():
  # 
  data = CreateRequest("DeviceOn")
  data["args"].append({})
  data["args"][0]["housedevicecode"] = "A1"
  data["args"][0]["dimamount"] = 0

  # Convert the payload structure into json text.
  # Effectively this serializes the payload.
  #print "raw json:", data
  json_data = json.JSONEncoder().encode(data)

  # Create a socket connection to the server
  sock = ConnectToServer(Host)
  if sock is None:
    return

  # send status request to server
  try:
    print "Sending status request:", json_data
    sock.sendall(json_data)

    # Receive data from the server and shut down
    #received = sock.recv(1024)
    json_data = ReadJson(sock)
    
    #print "Sent:     {}".format(data)
    #print "Received: {}".format(json_data)
    DisplayResponse(json_data)
  except Exception as ex:
    print str(ex)
  finally:
    sock.close()
        
# Test the status request command        
def StatusRequest():
  # This DOES NOT work. Why?
  data = "{ \"command\": \"StatusRequest\", \"args\": {\"a\": 1} }"
  
  # This DOES work. Why?
  data = CreateRequest("StatusRequest")

  # Convert the payload structure into json text.
  # Effectively this serializes the payload.
  #print "raw json:", data
  json_data = json.JSONEncoder().encode(data)

  # Create a socket connection to the server
  sock = ConnectToServer(Host)
  if sock is None:
    return

  # send status request to server
  try:
    print "Sending status request:", json_data
    sock.sendall(json_data)

    # Receive data from the server and shut down
    #received = sock.recv(1024)
    json_data = ReadJson(sock)
    
    #print "Sent:     {}".format(data)
    #print "Received: {}".format(json_data)
    DisplayResponse(json_data)
  except Exception as ex:
    print str(ex)
  finally:
    sock.close()

def LoadTimers():
  # New socket. 
  sock = ConnectToServer()
  if sock is None:
    return
  
  # JSON formatted payload to be sent to the tcpserver
  # data = \
    # '{ \
      # "command": "LoadTimers",  \
      # "args": { \
        # "housedevicecode": "a1", \
        # "ontime": "18:00", \
        # "offtime": "22:00", \
        # "daymask": "smtwtfs" \
        # } \
      # }'
      
  data = CreateRequest("LoadTimers")
  
  # For the LoadTimers command, args is a simple sequence/list of dict's where each dict
  # defines a timer initiator program.
  
  program = {\
    "housedevicecode": "a1", \
    "ontime": "18:00", \
    "offtime": "22:00", \
    "daymask": "smtwtfs", \
    "actionmacro": "macroname" }\

  program2 = {\
  "housedevicecode": "a2", \
  "ontime": "18:00", \
  "offtime": "22:00", \
  "daymask": "smtwtfs",
  "actionmacro": "macroname" }\
  
  program3 = {}
  program3["housedevicecode"] = "a3"
  program3["ontime"] = "15:30"
  program3["offtime"] = "23:30"
  program3["daymask"] = "smtwtfs"
  program3["actionmacro"] = "macroname"
    
  data["args"].append(program)
  data["args"].append(program2)
  data["args"].append(program3)
  
  # for i in range(0, 98):
    # data["args"].append(program)
  
  # Convert the payload structure into json text.
  # Effectively this serializes the payload.
  json_request = json.JSONEncoder().encode(data)

  try:
    # send data
    sock.sendall(json_request)

    # Receive data from the server and shut down
    #received = sock.recv(1024)
    response = ReadJson(sock)
  finally:
    sock.close()

  print "Sent:     {}".format(json_request)
  #print "Received: {}".format(json_data)
  DisplayResponse(response)
  
#
# Main
#
if __name__ == "__main__":
  #imPort pdb; pdb.set_trace()

  parser = OptionParser()
  parser.add_option("-s")
  parser.add_option("-p")
  (options, args) = parser.parse_args()
  #print options

  if options.s is not None:
    Host = options.s
  if options.p is not None:
    Port = int(options.p)

  # Try a status request command
  StatusRequest()

  # Try some timer programs
  #LoadTimers()
  
  DeviceOn()
