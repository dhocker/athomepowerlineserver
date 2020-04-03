# AtHomeServer API Module
For complete documentation of the AtHomeServer interface, see 
[here](https://github.com/dhocker/athomepowerlineserver/blob/master/readme-api.md).

# Module: ahps_api 
## Class: ServerRequest

###class ServerRequest(host="localhost", port=9999, verbose=True)
```python
from ahps.ahps_api import ServerRequest
request = ServerRequest()
```

### Class Methods
####create_request(command)
This is useful if you need to create a raw request.
```python
request = ServerRequest.create_request()
```

### Instance Methods
All instance methods use the create_request method to form a request.

####status_request()
```python
result = request.status_request()
```
result
```json
{
  "request": "StatusRequest",
  "date-time": "2019-06-25 16:30:18.080467",
  "server": "PerryM2/AtHomePowerlineServer",
  "server-version": "2019.0.0.1",
  "result-code": 0,
  "day-of-week": "1",
  "firmware-revision": "0.0.0.0",
  "message": "Success",
  "call-sequence": 5
}
```

###device_on(device_id, color=None, brightness=None)
```python
result = request.device_on(1)
```
result
```json
{
    "request": "On",
    "date-time": "2019-06-22 14:12:14.983421",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 1
}
```

###device_off(device_id)
```python
result = request.device_off(1)
```
result
```json
{
    "request": "Off",
    "date-time": "2019-06-22 14:17:46.370052",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 2
}
```

###all_devices_on()
```python
result = request.all_devices_on()
```
result
```json
{
    "request": "AllDevicesOn",
    "date-time": "2019-06-22 14:17:46.370052",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 2
}
```

###all_devices_off()
```python
result = request.all_devices_off()
```
result
```json
{
    "request": "AllDevicesOff",
    "date-time": "2019-06-22 14:17:46.370052",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 2
}
```

###define_device(device)
```python
device = {
    "description": "Define device test case",
    "device-name": "Meross Color Bulb - device under test",
    "device-location": "The Agency Studio",
    "device-mfg": "meross",
    "device-address": "19092014111.....................",
    "device-channel": 0,
    "device-color": "#00FF00",
    "device-brightness": 100
}
request.define_device(device)
```
result
```json
{
    "request": "DefineDevice",
    "date-time": "2020-03-29 11:53:19.601708",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "device-id": 26,
    "message": "Success",
    "call-sequence": 5
}
```

###update_device(device)
```python
device = {
    "device-id": 26,
    "description": "Define device test case",
    "device-name": "Meross Color Bulb - device under test",
    "device-location": "The Agency Studio",
    "device-mfg": "meross",
    "device-address": "19092014111.....................",
    "device-channel": 0,
    "device-color": "#00FF00",
    "device-brightness": 100
}
result = request.update_device(device)
```
result
```json
{
    "request": "UpdateDevice",
    "date-time": "2019-06-22 14:39:32.071068",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "device-id": 25,
    "message": "Success",
    "call-sequence": 4
}
```

###delete_device(device_id)
```python
result = request.delete_device(26)
```
result
```json
{
    "request": "DeleteDevice",
    "date-time": "2020-03-29 12:08:18.637120",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "device-id": "26",
    "message": "Success",
    "call-sequence": 6
}
```

###define_program(program)
```python
program = {
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
request.define_program(program)
```
result
```json
{
    "request": "DefineProgram",
    "date-time": "2020-03-29 12:28:14.197721",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "id": 10,
    "message": "",
    "call-sequence": 7
}
```

###update_program(program)
```python
program = {
    "id": 10,
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
request.update_program(program)
```
result
```json
{
    "request": "UpdateProgram",
    "date-time": "2020-03-29 12:34:02.103579",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "id": 10,
    "message": "",
    "call-sequence": 8
}
```

###delete_program(program_id)
```python
result = request.delete_program(10)
```
result
```json
{
    "request": "DeleteProgram",
    "date-time": "2020-03-29 12:35:38.531841",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "device-id": "10",
    "message": "",
    "call-sequence": 9
}
```

###define_action_group(group_name)
```python
result = request.define_action_group("group name")
```
result
```json
{
    "request": "DefineActionGroup",
    "date-time": "2020-03-29 15:51:54.561429",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "group-id": 12,
    "message": "Success",
    "call-sequence": 11
}
```

###update_action_group(group_id, group_name)
```python
result = request.update_action_group(12, "group name")
```
result
```json
{
    "request": "UpdateActionGroup",
    "date-time": "2020-03-29 15:55:37.848256",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "group-id": "12",
    "message": "Success",
    "call-sequence": 13
}
```

###delete_action_group(group_id)
```python
result = request.delete_action_group(12)
```
result
```json
{
    "request": "DeleteActionGroup",
    "date-time": "2020-03-29 16:05:15.038721",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "group-id": "12",
    "message": "Success",
    "call-sequence": 15
}
```

###query_action_group(group_id)
```python
result = request.query_action_group(12)
```
result
```json
{
    "request": "QueryActionGroup",
    "date-time": "2020-03-29 17:06:59.935416",
    "server": "PerryM2.local/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "group": {
        "id": 1,
        "name": "Foyer"
    },
    "message": "Success",
    "call-sequence": 17
}
```

###get_action_group_devices(group_id)
```python
result = request.get_action_group_devices(1)
```
result
```json
{
    "request": "QueryActionGroupDevices",
    "date-time": "2020-04-01 16:12:58.323014",
    "server": "PerryM2.attlocal.net/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "devices": [
    {
        "id": 28,
        "name": "Small Table (Meross Plug 3)",
        "location": "Foyer",
        "mfg": "meross",
        "address": "1907220924955625185048e1e901d533",
        "channel": 0,
        "color": "#ffffff",
        "brightness": 100,
        "updatetime": "2019-12-30 12:25:14.416311",
        "group_id": 1,
        "device_id": 28
    },
    {
        "id": 29,
        "name": "Drop Leaf Table (Meross Plug 4)",
        "location": "Foyer",
        "mfg": "meross",
        "address": "1907224198291625185048e1e901d51a",
        "channel": 0,
        "color": "#ffffff",
        "brightness": 100,
        "updatetime": "2020-01-27 11:45:59.498206",
        "group_id": 1,
        "device_id": 29
    }
    ],
    "message": "Success",
    "call-sequence": 1
}
```

###query_action_groups()
```python
result = request.query_action_groups()
```
result
```json
{
    "request": "QueryActionGroups",
    "date-time": "2020-04-01 16:22:57.446347",
    "server": "PerryM2.attlocal.net/AtHomePowerlineServer",
    "server-version": "2020.1.0.1",
    "result-code": 0,
    "groups": [
        {
          "id": 10,
          "name": "All"
        },
        {
          "id": 8,
          "name": "Breakfast Nook"
        },
        {
          "id": 11,
          "name": "Studio"
        },
        {
          "id": 7,
          "name": "Office"
        }
    ],
    "message": "Success",
    "call-sequence": 2
}
```

###query_available_devices_for_group_id(mfg_type)
```python
result = request.query_available_devices_for_group_id("tplink")
```
result
```json
{
  "request": "QueryAvailableDevices",
  "date-time": "2020-04-02 16:39:10.285970",
  "server": "PerryM2.local/AtHomePowerlineServer",
  "server-version": "2020.1.0.1",
  "result-code": 0,
  "devices": {
    "192.168.1.181": {
      "manufacturer": "TPLink",
      "model": "HS103(US)",
      "label": "HS103-1",
      "channels": 1,
      "type": "Plug"
    },
    "192.168.1.184": {
      "manufacturer": "TPLink",
      "model": "HS100(US)",
      "label": "HS100-2",
      "channels": 1,
      "type": "Plug"
    }
  },
  "message": "Success",
  "call-sequence": 3
}
```

###query_available_group_devices(group_id)
```python
result = request.query_available_group_devices(2)
```
result
```json
{
  "request": "QueryAvailableGroupDevices",
  "date-time": "2020-04-02 17:29:05.276762",
  "server": "PerryM2.local/AtHomePowerlineServer",
  "server-version": "2020.1.0.1",
  "result-code": 0,
  "devices": [
    {
      "id": 16,
      "name": "Window Seat Decorations",
      "location": "Breakfast Nook",
      "mfg": "x10",
      "address": "A4",
      "channel": 0,
      "color": "#ffffff",
      "brightness": 100,
      "updatetime": "2019-12-30 12:25:13.790636"
    },
    {
      "id": 11,
      "name": "Server (HS-100-1)",
      "location": "Dining Room",
      "mfg": "tplink",
      "address": "192.168.1.183",
      "channel": 0,
      "color": "#ffffff",
      "brightness": 100,
      "updatetime": "2019-12-30 12:25:13.841877"
    },
    {
      "id": 35,
      "name": "Meross Color Bulb - device under test",
      "location": "The Agency Studio",
      "mfg": "meross",
      "address": "19092014111.............",
      "channel": 0,
      "color": "#00FF00",
      "brightness": 100,
      "updatetime": "2020-03-24 15:40:36.742986"
    }
  ],
  "message": "Success",
  "call-sequence": 7
}
```

###query_available_programs_for_device_id(device_id)
```python
result = request.query_available_programs_for_device_id(35)
```
result
```json
{
  "request": "QueryAvailablePrograms",
  "date-time": "2020-04-03 11:39:39.314492",
  "server": "PerryM2.attlocal.net/AtHomePowerlineServer",
  "server-version": "2020.1.0.1",
  "result-code": 0,
  "programs": [
    {
      "id": 1,
      "name": "On Daily @ sunset - 45",
      "daymask": "MTWTFSS",
      "triggermethod": "sunset",
      "time": "1900-01-01 00:00:00",
      "offset": -45,
      "randomize": 0,
      "randomizeamount": 0,
      "command": "on",
      "color": "#ffffff",
      "brightness": 100,
      "updatetime": "2020-02-03 15:26:58.971095"
    },
    {
      "id": 2,
      "name": "On Daily @ sunset - 60",
      "daymask": "MTWTFSS",
      "triggermethod": "sunset",
      "time": "1900-01-01 00:00:00",
      "offset": -60,
      "randomize": 0,
      "randomizeamount": 0,
      "command": "on",
      "color": "#ffffff",
      "brightness": 100,
      "updatetime": "2020-02-03 15:28:37.861480"
    }
  ],
  "message": "Success",
  "call-sequence": 2
}
```

###query_program_by_id(program_id)
```python
result = request.query_program_by_id(1)
```
result
```json
{
  "request": "QueryDeviceProgram",
  "date-time": "2020-04-03 11:54:11.063081",
  "server": "PerryM2.attlocal.net/AtHomePowerlineServer",
  "server-version": "2020.1.0.1",
  "result-code": 0,
  "program": {
    "id": 1,
    "name": "On Daily @ sunset - 45",
    "daymask": "MTWTFSS",
    "triggermethod": "sunset",
    "time": "1900-01-01 00:00:00",
    "offset": -45,
    "randomize": 0,
    "randomizeamount": 0,
    "command": "on",
    "color": "#ffffff",
    "brightness": 100,
    "updatetime": "2020-02-03 15:26:58.971095"
  },
  "message": "Success",
  "call-sequence": 3
}
```

###query_programs_for_device_id(parameters)
```python
result = request.query_programs_for_device_id(1)
```
result
```json
{
}
```

###query_devices()
```python
result = request.query_devices()
```
result
```json
{
  "request": "QueryDevices",
  "date-time": "2020-04-03 12:22:07.252186",
  "server": "PerryM2.attlocal.net/AtHomePowerlineServer",
  "server-version": "2020.1.0.1",
  "result-code": 0,
  "devices": [
    {
      "id": 16,
      "name": "Window Seat Decorations",
      "location": "Breakfast Nook",
      "mfg": "x10",
      "address": "A4",
      "channel": 0,
      "color": "#ffffff",
      "brightness": 100,
      "updatetime": "2019-12-30 12:25:13.790636",
      "type": "plug"
    },
    {
      "id": 35,
      "name": "Meross Color Bulb - device under test",
      "location": "The Agency Studio",
      "mfg": "meross",
      "address": "190920141110..................",
      "channel": 0,
      "color": "#00FF00",
      "brightness": 100,
      "updatetime": "2020-03-24 15:40:36.742986",
      "type": "bulb"
    }
  ],
  "message": "Success",
  "call-sequence": 10
}
```

###query_programs()
```python
result = request.query_programs()
```
result
```json
{
  "request": "QueryPrograms",
  "date-time": "2020-04-03 12:26:38.566738",
  "server": "PerryM2.attlocal.net/AtHomePowerlineServer",
  "server-version": "2020.1.0.1",
  "result-code": 0,
  "programs": [
    {
      "id": 1,
      "name": "On Daily @ sunset - 45",
      "daymask": "MTWTFSS",
      "triggermethod": "sunset",
      "time": "1900-01-01 00:00:00",
      "offset": -45,
      "randomize": 0,
      "randomizeamount": 0,
      "command": "on",
      "color": "#ffffff",
      "brightness": 100,
      "updatetime": "2020-02-03 15:26:58.971095"
    },
    {
      "id": 9,
      "name": "Test Off",
      "daymask": "MTWTFSS",
      "triggermethod": "clock-time",
      "time": "1900-01-01 12:24:00",
      "offset": 0,
      "randomize": 0,
      "randomizeamount": 0,
      "command": "off",
      "color": "#ffffff",
      "brightness": 100,
      "updatetime": "2020-02-26 12:22:50.372995"
    }
  ],
  "message": "Success",
  "call-sequence": 11
}
```

###api_function(parameters)
```python
result = request.api_function(12)
```
result
```json
{
}
```

###api_function(parameters)
```python
result = request.api_function(12)
```
result
```json
{
}
```

###open_request(request_json)
Use to send a customized raw JSON request. Refer to 
[AtHomeServer documentation](https://github.com/dhocker/athomepowerlineserver/blob/master/README.md).
for complete documentation of all requests.

```python
raw_request = {
    "request": "statusrequest",
    "args": {    
    }   
}
result = request.open_request(raw_request)
```
result
```json
{
  "request": "StatusRequest",
  "date-time": "2020-03-29 12:49:11.352620",
  "server": "PerryM2.local/AtHomePowerlineServer",
  "server-version": "2020.1.0.1",
  "result-code": 0,
  "day-of-week": "6",
  "firmware-revision": "0.0.0.0",
  "message": "Success",
  "call-sequence": 10
}
```

```python
result = request.device_dim(1, 50)
```
