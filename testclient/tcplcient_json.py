#
# AtHomPowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

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

#######################################################################
# Create an empty server request
# This is the safe way to create an empty request.
# The json module seems to be a bit finicky about the
# format of strings that it converts.
def CreateRequest(command):
  request = {}
  request["command"] = command
  # The args parameter is an dictionary.
  request["args"] = {}
  return request

#######################################################################
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
  
#######################################################################
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

#######################################################################
# Display a formatted response on the console        
def DisplayResponse(response):
    jr = json.loads(response)["X10Response"]
    
    print "Response for command:", jr["command"]
   
    # Loop through all of the entries in the response dict
    for k, v in jr.iteritems():
      if k != "command":
        print " ", k, ":", v
    print        

#######################################################################
# Send a command to the server
def SendCommand(data):
  # Convert the payload structure into json text.
  # Effectively this serializes the payload.
  #print "raw json:", data
  json_data = json.JSONEncoder().encode(data)

  # Create a socket connection to the server
  sock = ConnectToServer(Host)
  if sock is None:
    return None

  # send status request to server
  try:
    print "Sending request:", json_data
    sock.sendall(json_data)

    # Receive data from the server and shut down
    json_data = ReadJson(sock)
    
    #print "Sent:     {}".format(data)
    #print "Received: {}".format(json_data)
    DisplayResponse(json_data)
  except Exception as ex:
    print str(ex)
    json_data = None
  finally:
    sock.close()

  return json_data
        
#######################################################################
# Test the Device On command        
def DeviceOn():
  # 
  data = CreateRequest("DeviceOn")
  data["args"]["housedevicecode"] = "A1"
  data["args"]["dimamount"] = 0

  SendCommand(data)
        
#######################################################################
# Test the Device Off command        
def DeviceOff():
  # 
  data = CreateRequest("DeviceOff")
  data["args"]["housedevicecode"] = "A1"
  data["args"]["dimamount"] = 0

  SendCommand(data)
        
#######################################################################
# Test the status request command        
def StatusRequest():
  # This DOES NOT work. Why?
  #data = "{ \"command\": \"StatusRequest\", \"args\": {\"a\": 1} }"
  
  # This DOES work. Why?
  data = CreateRequest("StatusRequest")

  SendCommand(data)

#######################################################################
def LoadTimers(): 
  # JSON formatted payload to be sent to the tcpserver
  # data = \
    # '{ \
      # "command": "LoadTimers",  \
      # "args": { \
        # "housedevicecode": "a1", \
        # "ontime": "18:00", \
        # "offtime": "22:00", \
        # "daymask": "mtwtfss" \
        # } \
      # }'
      
  data = CreateRequest("LoadTimers")
  
  # For the LoadTimers command, the args dictionary contains a single
  # "programs" key/value pair. The value is a simple sequence/list of dict's where each dict
  # defines a timer initiator program.
  data["args"]["programs"] = []
  
  program = {\
    "name": "program-a1", \
    "housedevicecode": "a1", \
    "ontime": "18:00", \
    "offtime": "22:00", \
    "daymask": "mtwtfss", \
    "actionmacro": "macroname" }\

  program2 = {\
  "name": "program-a2", \
  "housedevicecode": "a2", \
  "ontime": "18:00", \
  "offtime": "22:00", \
  "daymask": "mtwtfss",
  "actionmacro": "macroname" }\
  
  program3 = {}
  program3["name"] = "program-a3"
  program3["housedevicecode"] = "a3"
  program3["ontime"] = "15:30"
  program3["offtime"] = "23:30"
  program3["daymask"] = "mtwtfss"
  program3["actionmacro"] = "macroname"
  
  program4 = {\
    "name": "program-a4", \
    "housedevicecode": "a4", \
    "ontime": "18:00", \
    "offtime": "22:00", \
    "daymask": "mtwtf--", \
    "actionmacro": "macroname" }\
    
  data["args"]["programs"].append(program)
  data["args"]["programs"].append(program2)
  data["args"]["programs"].append(program3)
  data["args"]["programs"].append(program4)
  
  # for i in range(0, 98):
    # data["args"].append(program)

  SendCommand(data)    
  
#######################################################################
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
  LoadTimers()
  
  DeviceOn()

  DeviceOff()
