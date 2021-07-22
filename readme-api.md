# Programming: The TCP/IP Protocol

A client communicates with the server by sending a JSON formatted
request and the server returning a JSON formatted response. For each
request, the client opens a TCP/IP socket to the server, sends the
request, receives the response and closes the socket.

|                                                                                                      |                                                                                       |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Client                                                                                               | Server                                                                                |
| Open socket to server. The default port is 9999. This can be changed through the configuration file. |                                                                                       |
|                                                                                                      | Accept call from client. The server will accept a call on any host network interface. |
| Send JSON formatted request to server                                                                |                                                                                       |
|                                                                                                      | Receive request from client                                                           |
|                                                                                                      | Execute request                                                                       |
|                                                                                                      | Return JSON formatted response to client                                              |
| Receive response from server                                                                         |                                                                                       |
| Close socket to server                                                                               | Close socket to client                                                                |

## Standard Response Content

Each request generates a return response. The content of a response is
partially standard and partially request dependent. A request can add
any number of key/value pairs to the standard content. The standard
content is shown here.

JSON Format with standard content:
```json
{
    “request”: “StatusRequest”,
    “server”: “AtHomePowerlineServer”,
    “server-version”: “2020.0.0.1”,
    “result-code”: 0,
    “date-time”: “2014-01-29 11:04:06.093000”,
    “message”: “Message text”,
    “call-sequence”: 1
}
```
<table>
    <colgroup>
        <col style="width: 33%" />
        <col style="width: 33%" />
        <col style="width: 33%" />
    </colgroup>
    <tbody>
        <tr class="odd">
            <td>Key</td>
            <td>Value(s)</td>
            <td>Description</td>
        </tr>
        <tr class="even">
            <td>request</td>
            <td>StatusRequest</td>
            <td>Identifies the request for which the response is given.</td>
        </tr>
        <tr class="odd">
            <td>server</td>
            <td>AtHomePowerlineServer</td>
            <td>The name of the server yielding the response.</td>
        </tr>
        <tr class="even">
            <td>server-version</td>
            <td>2020.0.0.1</td>
            <td>The version of the responding server.</td>
        </tr>
        <tr class="odd">
            <td>result-code</td>
            <td>integer</td>
            <td>
                <div>
                <h4>TPLink and Meross Devices</h4>
                </div>
                <p>0 - The command was successfully executed.</p>
                <p>400 - Incorrectly formed request (e.g. missing or incorrect parameters)</p>
                <p>404 - Unknown command</p>
                <p>500 - Internal server error</p>
                <p>501 - Not implemented</p>
            </td>
        </tr>
        <tr class="even">
            <td>date-time</td>
            <td>Local time, ISO formatted</td>
            <td>The server time when the request was executed.</td>
        </tr>
        <tr class="odd">
            <td>error</td>
            <td>string</td>
            <td>Human readable text describing error condition. This parameter will only be present if the resultcode &gt; 0.</td>
        </tr>
        <tr class="even">
            <td>message</td>
            <td>string</td>
            <td>Human readable text providing extra details on the request. Consider this to be non-error text.</td>
        </tr>
        <tr class="odd">
            <td>call-sequence</td>
            <td>A sequential number</td>
            <td>An ever increasing number that identifies the order of the request. The sequence number is reset on every server start. Useful for client side logging.</td>
        </tr>
    </tbody>
</table>

Programmer Note: Typically, you are looking for a resultcode == 0. That
means your request was successful. Any non-zero resultcode means your
request failed for some reason. You will likely need to look at the
server console or the server log to determine why your request failed.

## AtHomeAPI Module
The easiest way to access the server is to use the AtHomeAPI module. Check out the
Readme.md file in the athomeserver/ahps directory.

## Requests

- [AllDevicesOff](#alldevicesoff)
- [AllDevicesOn](#alldeviceson)
- [AssignDevice](#assigndevice)
- [AssignProgram](#assignprogram)
- [AssignProgramToGroup](#assignprogramtogroup)
- [DefineActionGroup](#defineactiongroup)
- [DefineDevice](#definedevice)
- [DefineProgram](#defineprogram)
- [DeleteActionGroup](#deleteactiongroup)
- [DeleteActionGroupDevice](#deleteactiongroupdevice)
- [DeleteDevice](#deletedevice)
- [DeleteDeviceProgram](#deletedeviceprogram)
- [DiscoverDevices](#discoverdevices)
- [GroupOff](#groupoff)
- [GroupOn](#groupon)
- [Off or DeviceOff](#off)
- [On or DeviceOn](#on)
- [OnOffStatus]()
- [QueryActionGroup](#queryactiongroup)
- [QueryActionGroupDevices](#queryactiongroupdevices)
- [QueryActionGroups](#queryactiongroups)
- [QueryAvailableDevices](#queryavailabledevices)
- [QueryAvailableGroupDevices](#queryavailablegroupdevices)
- [QueryAvailablePrograms](#queryavailableprograms)
- [QueryDeviceProgram](#querydeviceprogram)
- [QueryDevicePrograms](#querydeviceprograms)
- [QueryDevices](#querydevices)
- [StatusRequest](#statusrequest)
- [UpdateActionGroup](#updateactiongroup)
- [UpdateDevice](#updatedevice)
- [UpdateProgram](#updateprogram)


### StatusRequest

The StatusRequest is useful as a server handshake.

#### Request
```json
{
    “request”: “StatusRequest”,
    “args”: {}
}
```
#### Response
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

### QueryDevices

Returns information about defined devices.

#### Request
For all devices
```json
{
    “request”: “QueryDevices”,
    “args”: {}
}
```
For a single device
```json
{
    "request": "QueryDevices",
    "args": {
        "device-id": "2"
    }
}
```
#### Response
For all devices
```json
{
    "request": "QueryDevices",
    "date-time": "2019-06-23 13:03:21.244097",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "devices": [
        {
          "id": 11,
          "name": "Device Name",
          "location": "Room",
          "type": "tplink",
          "on": false,
          "address": "192.168.1.1",
          "selected": 0,
          "updatetime": "2019-06-06 11:46:58.570884"
        },
        {
          "id": 16,
          "name": "Window Seat Decorations",
          "location": "Breakfast Nook",
          "type": "tplink",
          "address": "192.168.1.2",
          "selected": 0,
          "updatetime": "2019-06-06 11:46:58.591461"
        },
        ...
        ...
    ]
}
```
For a single device
```json
{
    "request": "QueryDevices",
    "date-time": "2019-06-23 13:06:45.587844",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "device": {
        "id": 2,
        "name": "Sofa Table",
        "location": "Hallway/Foyer",
        "type": "tplink",
        "address": "192.168.1.1",
        "selected": 1,
        "updatetime": "2019-06-06 11:46:58.528380"
    },
    "message": "Success",
    "call-sequence": 3
}
```   

### DefineDevice

Used to add a new device.

#### Request
```json
{
    "request": "DefineDevice",
    "args": {
        "device-name": "Device under test",
        "device-location": "Unknown test location",
        "device-type": "tplink",
        "device-address": "192.168.1.234",
        "device-selected": 0
    }
}
```

| args Key | Value(s) | Description |
|:---|:---|:---|
| device-name | string | The human readable name of the device |
| device-location | string | The human readable description of where the device is located |
| device-type | tplink or meross | The type of device |
| device-address | IP address, UUID | For a TPLink device, an IP address. For a Meross device, a UUID. |
| device-selected | 0 or 1 | Marks the device as in the selected group. |

#### Response
```json
{
    "request": "DefineDevice",
    "date-time": "2019-06-22 14:28:53.208809",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2020.0.0.1",
    "result-code": 0,
    "device-id": 26,
    "message": "Success",
    "call-sequence": 3
}
```
### UpdateDevice

Used to update the definition of an existing device.

#### Request
```json
{
    "request": "UpdateDevice",
    "args": {
        "device-id": 25,
        "device-name": "Device under test update 1",
        "device-location": "Unknown test location",
        "device-type": "tplink",
        "device-address": "192.168.1.234",
        "device-selected": 0
    }
}
```

| args Key | Value(s) | Description |
| :--- | :--- | :--- |
| device-id | integer | The device ID of the device to be updated. |
| device-name | string | The human readable name of the device |
| device-location | string | The human readable description of where the device is located |
| device-type | tplink or meross | The type of device |
| device-address | IP address, UUID | For a TPLink device, an IP address. For a Meross device, a UUID. |
| device-selected | 0 or 1 | Marks the device as in the selected group. |

#### Response
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

### DeleteDevice

#### Request
```json
{
    "request": "DeleteDevice",
    "args": {
        "device-id": "25"
    }
}
```
#### Response
```json
{
    "request": "DeleteDevice",
    "date-time": "2019-06-23 13:18:24.745503",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "device-id": "25",
    "message": "Success",
    "call-sequence": 6
}
```

### DefineProgram

A timer or device program is used to control devices. A timer program

* Defines when (on what day(s) and at what time) a timer event triggers.
* Identifies the device to be affected.
* Specifies what command is to be executed when the trigger occurs. 

Typically, two timer programs are defined. One turns a device on and the
other turns a device off.

There are several different methods for triggering a timer program. 

* clock-time
* sunset
* sunrise

The interesting case is the sunset/sunrise based case. You
can specify an event to occur relative to sunrise or sunset. For
example, you can create an event where the trigger occurs 10 minutes
before sunset. This would be useful for turning on a light at dusk. Or,
you might set a trigger event to occur a few minutes after sunrise. This
might be useful for turning off outside lights in the morning. The
obvious value of sunset/sunrise based events is that you do not have to
change them to accommodate the time of year.

As an aside, the Astral package is used to get sunrise/sunset times.

A timer program may also include a randomization factor for the trigger. 
This feature can be used to adjust a trigger event for a
more “human” behavior.

Timer programs are persisted in a Sqlite3 database in the Timers table.
They are loaded at server start up.

#### Request
```json
{
    "request": "DefineProgram",
    "args": {
        "name": "Program name",
        "device-id": "25",
        "day-mask": "MTWTFSS",
        "trigger-method": "sunset",
        "time": "12:00:00",
        "offset": "-60",
        "command": "on",
        "randomize": false,
        "randomize-amount": "0",
        "dimamount": "0"
    }
}
```
<table>
    <colgroup>
        <col style="width: 33%" />
        <col style="width: 33%" />
        <col style="width: 33%" />
    </colgroup>
    <tbody>
        <tr class="odd">
            <td>args Key</td>
            <td>Value(s)</td>
            <td>Description</td>
        </tr>
        <tr class="even">
            <td>name</td>
            <td>string</td>
            <td>Human readable name for the program.</td>
        </tr>
        <tr class="odd">
            <td>device-id</td>
            <td>integer</td>
            <td><p>The device ID of the device to which the program applies.</p></td>
        </tr>
        <tr class="even">
            <td>trigger-method</td>
            <td><p>none</p>
            <p>clock-time</p>
            <p>sunrise</p>
            <p>sunset</p></td>
            <td><p>Event is not used.</p>
            <p>Event triggered on local clock time.</p>
            <p>Event triggered relative to sunrise.</p>
            <p>Event triggered relative to sunset.</p></td>
        </tr>
        <tr class="odd">
            <td>time</td>
            <td>HH:MM</td>
            <td>Using a 24 hour clock, the time when the event triggers.</td>
        </tr>
        <tr class="even">
            <td>offset</td>
            <td>+/-n (minutes)</td>
            <td>Offset from sunrise/sunset for the event.</td>
        </tr>
        <tr class="odd">
            <td>randomize</td>
            <td>0 or 1</td>
            <td>0=false, 1=true. If true, randomize the trigger time using the randomize-amount value.</td>
        </tr>
        <tr class="even">
            <td>randomize-amount</td>
            <td>n (minutes)</td>
            <td>If randomize is true, the effective trigger time will be adjusted by a randomized value r (in minutes) where -amount &lt;= r &lt;= amount.</td>
        </tr>
        <tr class="odd">
            <td>day-mask</td>
            <td><p>mtwtfss (whole week)</p>
            <p>mtwtf-- (week days)</p>
            <p>-----ss (weekend days)</p></td>
            <td>The day(s) of the week when the program is effective. Starts with Monday and ends with Sunday. Days with letters are effective. Days with a dash (-) or a period (.) are not effective.</td>
        </tr>
        <tr class="even">
            <td>command</td>
            <td>
                <p>on</p>
                <p>off</p>
                <p>dim</p>
                <p>bright</p>
                <p>none</p>
            </td>
            <td>The name of the command to be executed when the start event occurs. 
                A value of none causes no action to be taken. If the named action is not found in the Actions table, no action is taken.</td>
        </tr>
        <tr class="odd">
            <td>dimamount</td>
            <td>0-100%</td>
            <td>A dim amount in percent. Not currently implemented.</td>
        </tr>
    </tbody>
</table>

#### Response
```json
    {
        "request": "DefineProgram",
        "date-time": "2019-06-23 11:19:12.893782",
        "server": "PerryM2/AtHomePowerlineServer",
        "server-version": "2019.0.0.1",
        "result-code": 0,
        "id": 50,
        "message": "Success",
        "call-sequence": 1
    }
```
1. The id property is the newly defined program ID.

### UpdateProgram

#### Request
```json
{
    "request": "UpdateProgram",
    "args": {
        "name": "name update",
        "device-id": "25",
        "day-mask": "MTWTFSS",
        "trigger-method": "sunset",
        "time": "12:00:00",
        "offset": "-60",
        "command": "on",
        "randomize": false,
        "randomize-amount": "0",
        "dimamount": "0",
        "id": 49
    }
}
```
1. The id property is the program ID.
2. The device-id property defines the subject of the timer program.
#### Response
```json
{
    "request": "UpdateProgram",
    "date-time": "2019-06-23 13:11:55.589249",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 4
}
```

### DeleteDeviceProgram

#### Request
```json
{
  "request": "DeleteDeviceProgram",
  "args": {
    "program-id": "99"
  }
}
```
#### Response
```json
{
  "request": "DeleteDeviceProgram",
  "date-time": "2019-06-25 08:54:19.782413",
  "server": "PerryM2/AtHomePowerlineServer",
  "server-version": "2019.0.0.1",
  "result-code": 0,
  "program-id": "99",
  "message": "Success",
  "call-sequence": 4
}
```

### QueryDevicePrograms

#### Request
```json
{
  "request": "QueryDevicePrograms",
  "args": {
    "device-id": "2"
  }
}
```
#### Response
```json
{
  "request": "QueryDevicePrograms",
  "date-time": "2019-06-25 17:05:17.160553",
  "server": "PerryM2/AtHomePowerlineServer",
  "server-version": "2019.0.0.1",
  "result-code": 0,
  "programs": [
    {
      "id": 3,
      "name": "Start All Days",
      "deviceid": 2,
      "daymask": "MTWTFSS",
      "triggermethod": "sunset",
      "time": "1900-01-01 17:45:00",
      "offset": -45,
      "randomize": 0,
      "randomizeamount": 0,
      "command": "on",
      "dimamount": 0,
      "args": "",
      "updatetime": "2019-05-18 10:25:16.042086"
    },
    {
      "id": 4,
      "name": "Stop All Days",
      "deviceid": 2,
      "daymask": "MTWTFSS",
      "triggermethod": "clock-time",
      "time": "1900-01-01 23:55:00",
      "offset": 0,
      "randomize": 0,
      "randomizeamount": 0,
      "command": "off",
      "dimamount": 0,
      "args": "0",
      "updatetime": "2019-06-07 15:35:07.248073"
    }
  ],
  "message": "Success",
  "call-sequence": 7
}
```

### QueryDeviceProgram
Query a single device program using its program ID.

#### Request
```json
{
  "request": "QueryDeviceProgram",
  "args": {
    "program-id": "3"
  }
}
```
#### Response
```json
{
  "request": "QueryDeviceProgram",
  "date-time": "2019-06-25 17:06:54.607671",
  "server": "PerryM2/AtHomePowerlineServer",
  "server-version": "2019.0.0.1",
  "result-code": 0,
  "program": {
    "id": 3,
    "name": "start 4-All Days",
    "deviceid": 2,
    "daymask": "MTWTFSS",
    "triggermethod": "sunset",
    "time": "1900-01-01 17:45:00",
    "offset": -45,
    "randomize": 0,
    "randomizeamount": 0,
    "command": "on",
    "dimamount": 0,
    "args": "",
    "updatetime": "2019-05-18 10:25:16.042086"
  },
  "message": "Success",
  "call-sequence": 8
}
```

### On

The On request is an immediate request that specifies a device to be
turned on.

#### Request
```json
{
    "request": "On",
    "args": {
        "device-id": "2",
        "dim-amount": "0"
    }
}
```

| args Key | Value | Description |
| --- | --- | --- |
| device-id | n | Identifies the device to be turned on.|
| dim-amount | nn | Dim amount expressed as a percent. Must be a value in the range 0-100. The server will convert this value into a something more meaningful to the actual device. |

#### Response

The On request returns a standard response.
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

### Off

The Off request is an immediate request that specifies a device to be
turned off.


#### Request
```json
{
    "request": "Off",
    "args": {
        "device-id": "2",
        "dim-amount": "0"
    }
}
```

| args Key | Value | Description |
|---|---|---|
| device-id | n | Identifies the device to be turned off.|
| dim-amount | nn | Dim amount expressed as a percent. Must be a value in the range 0-100. The server will convert this value into a something more meaningful to the actual device. |

#### Response

The Off request returns a standard response.
```json
{
    "request": "Off",
    "date-time": "2019-06-22 14:17:46.370052",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 2
}
```

### QueryAvailableDevices

Returns a list of available devices for a given device type.
Be aware that only TPLink/Kasa
and Meross devices can be discovered using this command.

#### Request
```json
{
    “request”: “QueryAvailableDevices”,
    “args”: {
      "type": "tplink"
    }
}
```
Valid types are tplink and meross.
#### Response
```json
{
    "request": "QueryAvailableDevices",
    "date-time": "2019-06-23 13:03:21.244097",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2020.0.0.1",
    "result-code": 0,
    "devices": {
      "address1": "name1",
      "address2": "name2"
    }
}
```

| Device Type | Address | Example |
| --- | --- | --- |
| tplink | IP address | 192.168.1.78 |
| meross | UUID | 1907226943690825185048e1e901c0b7 |

### DiscoverDevices
TPLink/Kasa and Meross devices are initially configured using their respective mobile/tablet apps. In order for these devices to be known by AHPS, they must be "discovered". When AHPS starts it runs the "discover devices" process so devices that have been configured will be found. However, if you add additional devices after AHPS starts you must rerun the "discover devices" process.

#### Request
```json
{
    “request”: “DiscoverDevices”
    }
}
```
#### Response
```json
{
    "request": "DiscoverDevices",
    "date-time": "2021-06-23 13:03:21.244097",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2021.1.0.3",
    "result-code": 0,
    "message": "Success"
    }
}
```

# Client Examples

## Test Client

The test client application in
**testclient/ahps\_client.py** provides several
examples of sending commands to the server and receiving command
responses.
