#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Test client for AtHomePowerlineServer
#
# ahps_client.py [-s hostname|hostaddress] [-p portnumber]
#

import socket
import sys
import json
import datetime
import time
from optparse import OptionParser

# Host and Port can be overriden by the -s and -p command line options
#Host, Port = "localHost", 9999
Host, Port = "hedwig", 9999
#Host, Port = "192.168.1.111", 9999

# ahps_client
# Sends and receives JSON formatted payloads

#######################################################################
# Create an empty server request
# This is the safe way to create an empty request.
# The json module seems to be a bit finicky about the
# format of strings that it converts.
def CreateRequest(command):
  request = {}
  request["request"] = command
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
    
    print "Response for request:", jr["request"]
   
    # Loop through all of the entries in the response dict
    for k, v in jr.iteritems():
      if k != "request":
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
# Test the Get Time command
def GetTime():
  #
  data = CreateRequest("GetTime")

  SendCommand(data)

#######################################################################
# Test the Set Time command
def SetTime():
  #
  data = CreateRequest("SetTime")

  SendCommand(data)

#######################################################################
# Test the Device On command        
def DeviceOn(house_device_code, dim_amount):
  # 
  data = CreateRequest("On")
  data["args"]["house-device-code"] = house_device_code
  data["args"]["dim-amount"] = dim_amount

  SendCommand(data)
        
#######################################################################
# Test the Device Off command        
def DeviceOff(house_device_code, dim_amount):
  # 
  data = CreateRequest("Off")
  data["args"]["house-device-code"] = house_device_code
  data["args"]["dim-amount"] = dim_amount

  SendCommand(data)

#######################################################################
# Test the Device Dim command
def DeviceDim(house_device_code, dim_amount):
  #
  data = CreateRequest("Dim")
  data["args"]["house-device-code"] = house_device_code
  data["args"]["dim-amount"] = dim_amount

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
  # JSON formatted payload to be sent to the AtHomePowerlineServer
  # data = \
    # '{ \
      # "command": "LoadTimers",  \
      # "args": { \
        # "house-device-code": "a1", \
        # "start-time": "18:00", \
        # "stop-time": "22:00", \
        # "day-mask": "mtwtfss" \
        # } \
      # }'
      
  data = CreateRequest("LoadTimers")
  
  # For the LoadTimers command, the args dictionary contains a single
  # "programs" key/value pair. The value is a simple sequence/list of dict's where each dict
  # defines a timer initiator program.
  data["args"]["programs"] = []

  # To facilitate testing, we make the start and stop times a short distance from now
  now = datetime.datetime.now()
  # 2 minutes from now
  td2 = datetime.timedelta(0, 0, 0, 0, 2)
  # 4 minutes from now
  td4 = datetime.timedelta(0, 0, 0, 0, 4)
  on_time = now + td2
  off_time = now + td4
  on_time_str = on_time.strftime("%H:%M")
  off_time_str = off_time.strftime("%H:%M")

  program = {
    "name": "program-a1", 
    "house-device-code": "a1", 
    "start-time": on_time_str, 
    "stop-time": off_time_str, 
    "day-mask": ".......", 
    "start-action": "action-1", 
    "stop-action": "action-2"}

  program2 = {
  "name": "program-c16", 
  "house-device-code": "c16", 
  "start-time": on_time_str, 
  "stop-time": off_time_str, 
  "day-mask": "mtwtfss",
  "start-action": "action-1", 
  "stop-action": "action-2" }
  
  program3 = {}
  program3["name"] = "program-a3"
  program3["house-device-code"] = "a3"
  program3["start-time"] = on_time_str
  program3["stop-time"] = off_time_str
  program3["day-mask"] = "mtwtfss"
  program3["start-action"] = "action-1"
  program3["stop-action"] = "action-2"
  
  program4 = {
    "name": "program-a4", 
    "house-device-code": "a4", 
    "start-time": on_time_str, 
    "stop-time": off_time_str, 
    "day-mask": "mtwtf--", 
    "start-action": "action-undefined", 
    "stop-action": "action-undefined"}
    
  data["args"]["programs"].append(program)
  data["args"]["programs"].append(program2)
  data["args"]["programs"].append(program3)
  data["args"]["programs"].append(program4)
  
  # for i in range(0, 98):
    # data["args"].append(program)

  SendCommand(data)    

#######################################################################
def LoadActions():
  data = CreateRequest("LoadActions")

  # For the LoadActions command, the args dictionary contains a single
  # "actions" key/value pair. The value is a simple sequence/list of dict's where each dict
  # defines an action.
  data["args"]["actions"] = []

  action1 = {
    "name": "action-1", 
    "command": "on", 
    "dim-amount": 0 }

  action2 = {
    "name": "action-2", 
    "command": "off", 
    "dim-amount": 0 }

  data["args"]["actions"].append(action1)
  data["args"]["actions"].append(action2)

  SendCommand(data)

#######################################################################
#
# Main
#
if __name__ == "__main__":
  # Show license advertisement
  sys.path.append("../")
  import disclaimer.Disclaimer
  disclaimer.Disclaimer.DisplayDisclaimer()

  #import pdb; pdb.set_trace()

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

  # Test the time requests
  #SetTime()
  #GetTime()

  # Try some timer programs
  #LoadTimers()

  #LoadActions()

  print "A7 on"
  DeviceOn("A7", 0)

  print "sleep 10"
  time.sleep(10)

  print "A7 dim 25"
  DeviceDim("A7", 25)

  print "sleep 5"
  time.sleep(5)

  print "A7 off"
  DeviceOff("A7", 0)
