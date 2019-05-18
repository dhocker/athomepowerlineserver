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
# Host, Port = "localHost", 9999
Host, Port = "localhost", 9999
# Host, Port = "192.168.1.111", 9999
Verbose = True


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
        print("Unable to connect to server:", Host, Port)
        print(str(ex))

    return None


#######################################################################
# Read a JSON payload from a socket
def ReadJson(sock):
    depth = 0
    json_data = ""

    while (True):
        c = sock.recv(1).decode()
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
    if Verbose:
        jr = json.loads(response)["X10Response"]

        print("Response for request:", jr["request"])

        # Loop through all of the entries in the response dict
        for k, v in jr.items():
            if k != "request":
                print(" ", k, ":", v)
        print()


#######################################################################
# Send a command to the server
def SendCommand(data):
    # Convert the payload structure into json text.
    # Effectively this serializes the payload.
    # print "raw json:", data
    json_data = json.JSONEncoder().encode(data).encode()

    # Create a socket connection to the server
    sock = ConnectToServer(Host)
    if sock is None:
        return None

    # send status request to server
    try:
        print("Sending request:", json_data)
        sock.sendall(json_data)

        # Receive data from the server and shut down
        json_data = ReadJson(sock)

        # print "Sent:     {}".format(data)
        # print "Received: {}".format(json_data)
        DisplayResponse(json_data)
    except Exception as ex:
        print(str(ex))
        json_data = None
    finally:
        sock.close()

    return json.loads(json_data)["X10Response"]


#######################################################################
# Test the Get Time command
def GetTime():
    #
    data = CreateRequest("GetTime")

    return SendCommand(data)


#######################################################################
# Test the Set Time command
def SetTime():
    #
    data = CreateRequest("SetTime")

    return SendCommand(data)


#######################################################################
# Test the Device On command        
def DeviceOn(house_device_code, dim_amount):
    #
    data = CreateRequest("On")
    data["args"]["device-id"] = house_device_code
    data["args"]["dim-amount"] = dim_amount

    return SendCommand(data)


#######################################################################
# Test the Device Off command        
def DeviceOff(house_device_code, dim_amount):
    #
    data = CreateRequest("Off")
    data["args"]["device-id"] = house_device_code
    data["args"]["dim-amount"] = dim_amount

    return SendCommand(data)


#######################################################################
# Test the Device Dim command
def DeviceDim(house_device_code, dim_amount):
    #
    data = CreateRequest("Dim")
    data["args"]["house-device-code"] = house_device_code
    data["args"]["dim-amount"] = dim_amount

    return SendCommand(data)


#######################################################################
# Test the Device Bright command
def DeviceBright(house_device_code, bright_amount):
    #
    data = CreateRequest("Bright")
    data["args"]["house-device-code"] = house_device_code
    data["args"]["bright-amount"] = bright_amount

    return SendCommand(data)


#######################################################################
# Test the Device All Units Off command
def DeviceAllUnitsOff(house_code):
    #
    data = CreateRequest("AllUnitsOff")
    data["args"]["house-code"] = house_code

    return SendCommand(data)


#######################################################################
# Test the Device All Light Off command
def DeviceAllLightsOff(house_code):
    #
    data = CreateRequest("AllLightsOff")
    data["args"]["house-code"] = house_code

    return SendCommand(data)


#######################################################################
# Test the status request command        
def StatusRequest():
    # This DOES NOT work. Why?
    # data = "{ \"command\": \"StatusRequest\", \"args\": {\"a\": 1} }"

    # This DOES work. Why?
    data = CreateRequest("StatusRequest")

    return SendCommand(data)


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

    """
    name, device_id, day_mask, start_trigger_method, start_time,
                     start_offset, stop_trigger_method, stop_time, stop_offset,
                     start_action, stop_action, start_randomize, start_randomize_amount,
                     stop_randomize, stop_randomize_amount
    """

    program = create_program("program-a1",
                             1,
                             "mtwtfss",
                             "clock-time",
                             on_time,
                             0,
                             "clock-time",
                             off_time,
                             0,
                             "action-1",
                             "action-2",
                             0,
                             0,
                             0,
                             0)

    program2 = create_program("program-c16",
                              2,
                              "mtwtfss",
                              "clock-time",
                              on_time,
                              0,
                              "clock-time",
                              off_time,
                              0,
                              "action-1",
                              "action-2",
                              0,
                              0,
                              0,
                              0)

    program3 = create_program("program-a3",
                              3,
                              "mtwtfss",
                              "clock-time",
                              on_time,
                              0,
                              "clock-time",
                              off_time,
                              0,
                              "action-3",
                              "action-4",
                              0,
                              0,
                              0,
                              0)

    program4 = create_program("program-a4",
                              3,
                              "mtwtf--",
                              "clock-time",
                              on_time,
                              0,
                              "clock-time",
                              off_time,
                              0,
                              "action-undefined",
                              "action-undefined",
                              0,
                              0,
                              0,
                              0)

    data["args"]["programs"].append(program)
    data["args"]["programs"].append(program2)
    data["args"]["programs"].append(program3)
    data["args"]["programs"].append(program4)

    return SendCommand(data)


def create_program(name, device_id, day_mask, start_trigger_method, start_time,
                   start_offset, stop_trigger_method, stop_time, stop_offset,
                   start_action, stop_action, start_randomize, start_randomize_amount,
                   stop_randomize, stop_randomize_amount):
    timer_program = {
        "name": name,
        "device-id": str(device_id),
        "day-mask": day_mask,
        "start-trigger-method": start_trigger_method,
        "start-time": start_time.strftime("%H:%M"),
        "start-time-offset": str(start_offset),
        "stop-trigger-method": stop_trigger_method,
        "stop-time": stop_time.strftime("%H:%M"),
        "stop-time-offset": str(stop_offset),
        "start-action": start_action,
        "stop-action": stop_action,
        "start-randomize": True if start_randomize else False,
        "start-randomize-amount": str(start_randomize_amount),
        "stop-randomize": True if stop_randomize else False,
        "stop-randomize-amount": str(stop_randomize_amount)
    }
    return timer_program


def create_timer_program(name, device_id, day_mask, trigger_method, trigger_time,
                   offset, action, randomize, randomize_amount, dimamount):
    timer_program = {
        "name": name,
        "device-id": str(device_id),
        "day-mask": day_mask,
        "trigger-method": trigger_method,
        "time": trigger_time.strftime("%H:%M"),
        "offset": str(offset),
        "action": action,
        "randomize": True if randomize else False,
        "randomize-amount": str(randomize_amount),
        "dimamount": str(dimamount)
    }
    return timer_program


def define_program(name, device_id, delta_time_min, action):

    data = CreateRequest("DefineProgram")

    # To facilitate testing, we make the start/stop times a short distance from now
    now = datetime.datetime.now()
    # x minutes from now
    td2 = datetime.timedelta(0, 0, 0, 0, delta_time_min)
    on_time = now + td2

    program = create_timer_program(name,
                             device_id,
                             "mtwtfss",
                             "clock-time",
                             on_time,
                             0,
                             action,
                             0,
                             0,
                             0)

    # For the DefineProgram command, the args dictionary contains
    # contains the program values
    data["args"] = program

    return SendCommand(data)


def update_program(id, name, device_id, delta_time_min, action):

    data = CreateRequest("UpdateProgram")

    # To facilitate testing, we make the start/stop times a short distance from now
    now = datetime.datetime.now()
    # x minutes from now
    td2 = datetime.timedelta(0, 0, 0, 0, delta_time_min)
    on_time = now + td2

    program = create_timer_program(name,
                             device_id,
                             "mtwtfss",
                             "clock-time",
                             on_time,
                             0,
                             action,
                             0,
                             0,
                             0)
    program["id"] = id

    # For the DefineProgram command, the args dictionary contains
    # contains the program values
    data["args"] = program

    return SendCommand(data)


def define_device(device_name, device_location, device_type, device_address, device_selected):
    data = CreateRequest("DefineDevice")
    data["args"]["device-name"] = device_name
    data["args"]["device-location"] = device_location
    data["args"]["device-type"] = device_type
    data["args"]["device-address"] = device_address
    data["args"]["device-selected"] = device_selected

    result = SendCommand(data)
    print(result)

def update_device(device_id, device_name, device_location, device_type, device_address, device_selected):
    data = CreateRequest("UpdateDevice")
    data["args"]["device-id"] = device_id
    data["args"]["device-name"] = device_name
    data["args"]["device-location"] = device_location
    data["args"]["device-type"] = device_type
    data["args"]["device-address"] = device_address
    data["args"]["device-selected"] = device_selected

    result = SendCommand(data)
    print(result)

def query_devices():
    data = CreateRequest("QueryDevices")
    result = SendCommand(data)
    if result:
        for dev in result["devices"]:
            print(json.dumps(dev, indent=4))


#######################################################################
#
# Main
#
if __name__ == "__main__":
    # Show license advertisement
    sys.path.append("../")
    import disclaimer.Disclaimer

    disclaimer.Disclaimer.DisplayDisclaimer()

    # import pdb; pdb.set_trace()

    parser = OptionParser()
    parser.add_option("-s")
    parser.add_option("-p")
    (options, args) = parser.parse_args()
    # print options

    if options.s is not None:
        Host = options.s
    if options.p is not None:
        Port = int(options.p)

    # Try a status request command
    StatusRequest()

    # Test define device
    # define_device("test-device-1", "Test location for device 1", "x10", "L2", False)
    # define_device("test-device-2", "Test location for DEVICE 2", "tplink", "192.168.1.181", True)

    # Test update device (device IDs from test defines)
    # update_device(19, "test-device-1", "Test address changed 2", "x10", "L3", False)
    # update_device(20, "test-device-222", "Test device name changed", "tplink", "192.168.1.181", True)

    # Test query devices
    # query_devices()

    # Test the time requests
    # SetTime()
    # GetTime()

    # Try some timer programs
    # on in 2 min, off in 3 min
    # define_program("Test program B1 on", 1, 2, "on")
    # define_program("Test program B1 off", 1, 3, "off")
    update_program(37, "Test program A11 on", 18, 2, "on")
    update_program(38, "Test program A11 off", 18, 3, "off")

    # LoadActions()

    # print("Device 5 on 50")
    # DeviceOn("5", 50)
    #
    # print "sleep 10"
    # time.sleep(10)
    #
    # print("A7 bright 50")
    # DeviceBright("a7", 50)
    #
    # print "A7 dim 50"
    # DeviceDim("A7", 50)
    #
    # print("sleep 5")
    # time.sleep(5)
    #
    # print("Device 5 off")
    # DeviceOff("5", 0)

    # print "sleep 10"
    # time.sleep(10)

    # print("All units off A")
    # DeviceAllUnitsOff("A")
    # print "All units off P"
    # DeviceAllUnitsOff("P")

    # print "All lights off"
    # DeviceAllLightsOff("A")
