#AHPS Test Client
AtHomePowerlineServer (AHPS) Copyright © 2014, 2020 Dave Hocker (AtHomeX10@gmail.com)
Version 2020.1.0.1

This program comes with ABSOLUTELY NO WARRANTY; for details see the LICENSE file.
This is free software, and you are welcome to redistribute it
under certain conditions; see the LICENSE file for details.

#Command Line Tool
This is a command line tool that can be used to test and interact with the
AHPS server. It also serves as an example of how to use the AHPS API modue 
(ahps_api.py).

```
python3 ahps_client.py request [request-args...]
```
Example:
```
python3 ahps_client.py help all
python3 ahps_client.py statusrequest
```

#Help - Request List

Legend
* All request names are case insensitive
* device-id is the unique identifier for a device
* program-id is the unique identifier for a timer/trigger program
* group-id is the unique identifier for a device group
* <file_name.json> is a JSON formatted file

##alldevicesoff
Turn all devices off
```
Syntax: alldevicesoff
```
##alldeviceson
Turn all devices on
```
Syntax: alldeviceson
```
##assigndevice
Assign a device to a group
```
Syntax: assigndevice group-id device-id
```
##assignprogram
Assign a program to a device
```
Syntax: assignprogram device-id program-id
```
##assignprogramtogroup
Assign a program to a device group
```
Syntax: assignprogramtogroup group-id program-id
```
##definedevice
Define a new device using a JSON formatted input file
```
Syntax: definedevice <new_device.json>
```
##definegroup
Define a new device group
```
Syntax: definegroup group-name
```
##defineprogram
Define a new program
```
Syntax: defineprogram <new_program.json>
```
##deletedevice
Delete a device by ID
```
Syntax: deletedevice device-id
```
##deletedeviceprogram
Delete a program from a device
```
Syntax: deletedeviceprogram device-id program-id
```
##deletegroup
Delete a device group
```
Syntax: deletegroup group-id
```
##deletegroupdevice
Delete a device from a group
```
Syntax: deletegroupdevice group-id device-id
```
##deleteprogram
Delete a program
```
Syntax: deleteprogram program-id
```
##deviceoff
Turn a device off
```
Syntax: deviceoff device-id
```
##deviceon
Turn a device on
```
Syntax: deviceon device-id
```
##groupoff
Turn off all devices in a group
```
Syntax: deviceoff group-id
```
##groupon
Turn on all devices in a group
```
Syntax: groupon group-id
```
##help
Help for one or all requests
```
Syntax: help [requestname | all | *] {md}
```
##off
Turn a device off
```
Syntax: off device-id
```
##on
Turn a device on
```
Syntax: on device-id
```
##queryavailablegroupdevices
List all devices available for assignment to a group
```
Syntax: queryavailablegroupdevices group-id
```
##queryavailablemfgdevices
List all devices of a manufacturer/type
```
Syntax: queryavailablemfgdevices mfg-or-type
```
##queryavailableprograms
List all programs available for assignment to a device
```
Syntax: queryavailableprograms device-id
```
##querydevice
List a device by ID
```
Syntax: querydevice device-id
```
##querydeviceprogram
List program details for a program ID
```
Syntax: querydeviceprogram program-id
```
##querydeviceprograms
List all programs for a device ID
```
Syntax: querydeviceprograms device-id
```
##querydevices
List all devices with details
```
Syntax: querydevices
```
##querygroup
List device group details
```
Syntax: querygroup group-id
```
##querygroupdevices
List devices in a group
```
Syntax: querygroupdevices group-id
```
##querygroups
List all groups
```
Syntax: querygroups
```
##queryprogram
List program details for a program ID
```
Syntax: queryprogram program-id
```
##queryprograms
List all programs
```
Syntax: queryprograms device-id
```
##request
A raw request in JSON format
```
Syntax: request <request_file.json>
```
##statusrequest
Returns the status of the server
```
Syntax: StatusRequest
```
##updatedevice
Update a device definition using a JSON formatted input file
```
Syntax: updatedevice <update_device.json>
```
##updategroup
Update a group
```
Syntax: updategroup group-id group-name
```
##updateprogram
Update a program
```
Syntax: updateprogram <update_program.json>
```

#File Examples
##New Device
```
{
  "description": "Define device test case",
  "device-name": "Meross Color Bulb - device under test",
  "device-location": "The Agency Studio",
  "device-mfg": "meross",
  "device-address": "19092014111.....................",
  "device-channel": 0,
  "device-color": "#00FF00",
  "device-brightness": 100
}
```
##Update Device
```
{
  "description": "Update device test case",
  "device-id": 35,
  "device-name": "Meross Color Bulb - update 1",
  "device-location": "Unknown test location",
  "device-mfg": "meross",
  "device-address": "19092014111.....................",
  "device-channel": 0,
  "device-color": "#0000FF",
  "device-brightness": 100
}
```
##New Program
```
{
  "name": "name",
  "day-mask": "MTWTFSS",
  "trigger-method": "sunset",
  "time": "12:00:00",
  "offset": -60,
  "command": "on",
  "randomize": 0,
  "randomize-amount": 0,
  "color": "#ffffff",
  "brightness": 100
}
```
##Update Program
```
{
  "id": 49,
  "name": "name update",
  "day-mask": "MTWTFSS",
  "trigger-method": "sunset",
  "time": "12:00:00",
  "offset": -60,
  "command": "on",
  "randomize": 0,
  "randomize-amount": 0,
  "color": "#ffffff",
  "brightness": 100
}
```
