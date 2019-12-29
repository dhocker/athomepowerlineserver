# AtHomePowerlineServer

Copyright © 2014, 2020 Dave Hocker (<AtHomeX10@gmail.com>)

# Overview

The original version of AtHomePowerlineServer was written for X10 
controllers and modules.
In the world of X10, most of the power line controllers like the
CM11/CM11A have been around for years. The majority of the sophisticated
X10 management applications run on a PC or Mac and more or less use the
power line controller as a relatively “dumb” controller. There are a
number of problems with the current configurations that the
AtHomePowerlineServer aims to address.

First, the AtHomePowerline server is designed to run on a light weight
system (e.g. a Raspberry Pi v1, v2, v3, v4 or Zero W) that can be run
head-less and fan-less. This is as opposed to a PC or Mac based
solution. The small size of such a system like the Raspberry Pi allows
it to be positioned more freely (ideally, close to the breaker panel).
And, a Raspberry Pi system can be assembled for considerably less than a
PC. While the server was designed to run on a lightweight system, it
will run on any system that supports Python 3.5 or later (including
Windows).

Second, the communication mechanism to the AtHomePowerlineServer is
TCP/IP (over Ethernet). A light weight system like the Raspberry Pi
supports many WiFi USB interfaces and the later versions of the RPi have
integrated WiFi interfaces (e.g. RPi 3, RPi 4, RPi Zero W).
This further improves the freedom of
location for the X10 controller. In the past, the distance between a PC
and the X10 controller was gated by the need for physical wiring and
RS-232 limitations. With the AtHomePowerlineServer architecture, this
limitation is effectively eliminated. See Illustraion 1.

Recently, the server was extended to support a new class of WiFi based
switches and lights. This provides support for a number of TPLink/Kasa
WiFi devices and Meross WiFi devices. These WiFi devices are less expensive
than X10 modules and they are easier to position.

Finally, the AtHomePowerlineServer application is open source. Anyone
can fork it and build upon it.

The remainder of this document describes:

  - Supported devices
  - Installation
  - Configuration
  - Programming interface

While the functionality of the AtHomePowerlineServer is designed with
knowledge of the CM11/CM11A architecture, it does not really match that
architecture. The AtHomePowerlineServer is an abstraction of the
capabilities of the CM11/CM11A. The CM11 has initiators and actions.
Devices are by definition X10 modules. Initiatators define start and stop
timers. Actions describe X10 commands. 

AtHomePowerlineServer has devices and timer programs. A device is an X10
module, a TPLink/Kasa WiFi device or a Meross WiFi device.
A timer program defines a trigger and a
command/action to be executed when the trigger fires. Commands are logcial
actions like On and Off. Essentially, AtHomePowerlineServer is independent
of the actual hardware devices.

# License

The server is licensed under the GNU General Public License v3 as
published by the Free Software Foundation, Inc.. See the LICENSE file
for the full text of the license.

# Source Code

The server was originally written completely in Python 2.7 but has since
been converted to Python 3 (3.5 or later). The source
code can be found on [GitHub](https://github.com/dhocker/athomepowerlineserver.git).

# Attribution
This project depends on the following Python packages.
Many thanks to these contributors.

[TPLink Python Library](https://github.com/GadgetReactor/pyHS100) by GadgetReactor.

[Meross Python Library](https://github.com/albertogeniola/MerossIot) by Alberto Geniola.

# Supported Devices
## X10
### Controllers
* [XTB-232](http://jvde.us/xtb-232.htm)
* CM11/CM11a
## X10 Modules
* AM465 Lamp
* AM466 Appliance
* AM486 Appliance

## TPLink/Kasa WiFi Modules
### [Smart Plugs](https://www.kasasmart.com/us/products/smart-plugs)
* HS100
* HS103
* HS105
* HS107
* HS110

### [Smart Bulbs](https://www.kasasmart.com/us/products/smart-lighting)
* LB130

## Meross Devices
[WiFi Devices](https://www.meross.com/)

Currently, only channel 0 is supported.

## WiFi Plugs
* MSS110
* MSS210 (untested)
## WiFi Bulbs
* MSL120 (untested, on/off only)

# Installation

## Basic Steps for Raspbian

Open a terminal window and install prerequisites.

```bash
sudo apt-get install python-dev python-pip python3-pip
sudo pip install virtualenv
sudo pip install virtualenvwrapper
mkdir ~/Virtualenvs #(or similarly named directory for holding virtual environments).
mkdir ~/rpi
```

Add the following lines to the bottom of ~/.bashrc.

```bash
export WORKON_HOME=~/Virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```
This will set up virtualenvwrapper.

Clone the repository from GitHub. Under Raspbian the
recommended location for cloning is /home/pi/rpi/athomeserver. Using
this directory name will minimize the changes you will need to make
to the init.d script.

```bash
cd ~/rpi
git clone https://github.com/dhocker/athomepowerlineserver.git athomeserver
cd athomeserver
```

Create a virtual environment named athomeserver:
```bash
mkvirtualenv -p python3 -r requirements.txt athomeserver
```

Copy the file sample AtHomePowerlineServer.example.conf to
AtHomePowerlineServer.conf.

Edit the AtHomePowerlineServer.conf configuration file as needed.
Generally you will need to edit the ComPort parameter if you are
using an X10 type of controller. Also, change the
location parameters (city, longitude, latitude) so sunrise/sunset can
be accurately determined.

Move the AtHomePowerlineServer.conf file to the location identified
by section [Files and Their Location](files-and-their-location). If you put the file in /etc, use sudo
to move/copy the file so that it has root ownership.

If for some reason you have an existing database, Move or copy the
AtHomePowerlineServer.sqlite3 file to the location identified by
section [Files and Their Location](files-and-their-location).
Be sure to use sudo so that the
copied/moved file will belong to root. Otherwise, you will have to
“chown” the copied file to root ownership. If this a new install,
AtHomePowerlineServer will create the database when needed.

## Files and Their Location

There are two key files:

  - AtHomePowerlineServer.conf – the configuration file
  - AtHomePowerlineServer.sqlite3 – the database file

These files are kept in OS dependent locations. AtHomePowerlineServer
automatically creates the database file (if it does not exist), so there
is little to worry about there.

### Linux Based Systems

On Linux based systems like Raspbian, the key files are
kept in traditional locations.

|               |                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------- |
| File          | File Path                                                                                       |
| Configuration | \<home\>/AtHomePowerlineServer.conf or /etc/AtHomePowerlineServer.conf                          |
| Database      | \<DatabasePath\>/AtHomePowerlineServer.sqlite3. /var/local/athomeserver is a reasonable choice. |
| Logfile       | \<Logfile\> entry in AtHomePowerlineServer.conf                                                 |

\<home\> is the path to AtHomePowerlineServer.py file.

\<DatabasePath\> is the path specified by the AtHomePowerlineServer.conf
DatabasePath entry.

\<LogFile\> is the path and file name specified by the
AtHomePowerlineServer.conf LogFile entry.

Note that a configuration file in \<home\> takes precedent over one in
/etc.

### Windows

On Windows based systems the configuration file and the database file
are kept in the following locations.

|               |                                                                                                                             |
| ------------- | --------------------------------------------------------------------------------------------------------------------------- |
| File          | File Path                                                                                                                   |
| Configuration | Home directory of the AtHomePowerlineServer application. This will be the directory where AtHomePowerlineServer.py resides. |
| Database      | c:\\users\\username\\AppData\\Local\\AtHomePowerlineServer\\AtHomePowerlineServer.sqlite3                                   |

## Configuration File
### Organization

The configuration file is named AtHomePowerlineServer.conf. The contents
are JSON formatted. Use AtHomePowerlineServer.example.conf as a
template.

<table>
    <colgroup>
        <col style="width: 50%" />
        <col style="width: 50%" />
    </colgroup>
    <tbody>
        <tr class="odd">
            <td>Parameter/Key</td>
            <td>Description</td>
        </tr>
        <tr class="even">
            <td>Drivers</td>
            <td>
            <p>
                Maps devices to drivers. Currently, there are 4 available drivers.
                <ul>
                    <li>Dummy – A simulated controller. This is good for testing your installation.</li>
                    <li>XTB232 - The XTB-232 controller from JV Digital Engineering. Also works for CM11/CM11A.</li>
                    <li>TPLink – Covers most TPLink/Kasa smart devices.</li>
                    <li>Meross – Covers Meross WiFi devices.</li>
                </ul>
            </p>
            <p>
                Supported Devices
                <ul>
                    <li>X10</li>
                    <li>X10-appliance</li>
                    <li>X10-lamp</li>
                    <li>TPLink</li>
                    <li>HS100</li>
                    <li>HS103</li>
                    <li>HS105</li>
                    <li>HS107</li>
                    <li>HS110</li>
                    <li>HS200</li>
                    <li>HS210</li>
                    <li>HS220</li>
                    <li>smartplug</li>
                    <li>smartswitch</li>
                    <li>smartbulb</li>
                    <li>Meross</li>
                    <li>MSS110</li>
                </ul>
                See example below.
            </p>
        </tr>
        <tr class="odd">
            <td>ComPort</td>
            <td>The name of the port where the XTB232/CM11/CM11A X10 controller is attached.
            Under Windows this will be something like COM3.
            Under Raspbian it will be something like “/dev/ttyUSB0” (this is for a USB-Serial converter).</td>
        </tr>
        <tr class="even">
            <td>Port</td>
            <td>The TCP/IP port that the server is to listen on.</td>
        </tr>
        <tr class="odd">
            <td>LogFile</td>
            <td>The full path and name of the log file.</td>
        </tr>
        <tr class="even">
            <td>LogConsole</td>
            <td>True/False. Log to both console and file. Useful when running the server from a terminal window or from an IDE like PyCharm.</td>
        </tr>
        <tr class="odd">
            <td>LogLevel</td>
            <td><p>Degree of logging verbosity.</p>
            <p>DEBUG</p>
            <p>INFO</p>
            <p>WARN</p>
            <p>ERROR</p>
        </td>
        </tr>
        <tr class="even">
            <td>DatabasePath</td>
            <td>The location where the database will be kept. The name of the database file is always AtHomePowerlineServer.sqlite3 and the full path/name will be &lt;DatabasePath&gt;/AtHomePowerlineServer.sqlite3.</td>
        </tr>
        <tr class="odd">
            <td>City</td>
            <td>The city where the installation is located. City, latitude and longitude are used for accurately calculating the sunset and sunrise (using the astral package).</td>
        </tr>
        <tr class="even">
            <td>Latitude</td>
            <td>The latitude of installation.</td>
        </tr>
        <tr class="odd">
            <td>Longitude</td>
            <td>The longitude of the installation.</td>
        </tr>
        <tr class="even">
            <td>MerossEmail</td>
            <td>The email you used to set up your Meross account.</td>
        </tr>
        <tr class="odd">
            <td>Meross Password</td>
            <td>The password to your Meross account. See notes below discussing security.</td>
        </tr>
    </tbody>
</table>

### Example
```json
{
  "Configuration":
  {
    "Drivers": {
        "X10": "XTB232",
        "X10-appliance": "XTB232",
        "X10-lamp": "XTB232",
        "TPLink": "TPLink",
        "HS100": "TPLink",
        "HS103": "TPLink",
        "HS105": "TPLink",
        "HS107": "TPLink",
        "SmartPlug": "TPLink",
        "SmartSwitch": "TPLink",
        "SmartBulb": "TPLink",
        "Meross": "Meross",
        "MSS110": "Meross",
        "CustomDevice": "Dummy"
    },
    "ComPort": "/dev/tty.usbserial",
    "Port": 9999,
    "LogFile": "AtHomePowerlineServer.log",
    "LogConsole": "True",
    "LogLevel": "DEBUG",
    "DatabasePath": "",
    "City": "Houston",
    "Latitude": "29.9947",
    "Longitude": "-95.6675",
    "MerossEmail": "your Meross email",
    "MerossPassword": "your Meross account password"
   }
}
```

### Notes
If your are using Meross devices, you should set the permissions of the
configuration file to limit access. At a minimum, you should disallow
any access by "everyone". Under Linux, you should at least chmod the
file to permissions something like 640 or even the more restrictive 600.
Under Windows, you should remove "Everyone" from the file's permissions.

If you are using the [At Home Control](https://github.com/dhocker/athomefrb)
web client, you will find that it only supports
X10, TPLink and Meross device drivers. The X10 driver will work with all
X10 devices, the TPLink driver will work with most TPLink/Kasa devices and
the Meross driver will work with Meross WiFi plugs and bulbs.

## Running the Server

### Raspbian

#### As an Application

Start the server:
```bash
sudo python AtHomePowerlineServer.py
```

#### As a Daemon

This technique will set up AtHomePowerlineServer so that it
automatically starts when Raspbian boots up.

Change the AtHomePowerlineServerD.sh script as needed.
* Where you
have cloned the source code (approximately line 24). If you cloned
the source code into the recommended location no changes should be
required.
* The path to your virtual environment.

Run:
```bash
installD.sh
```

If you want to uninstall the daemon run:
```bash
uninstallD.sh
```

### Windows

AtHomePowerlineServer can be run as an ordinary Python application.
Change into the home directory and run:
```
python AtHomePowerlineServer.py
```

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
    “error”: “Error description”,
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
                <p>0 - The command was successfully executed.</p>
                <p>1 - Time out waiting for checksum from controller.</p>
                <p>2 - Time out waiting for interface ready from controller.</p>
                <p>3 - Ack was not received from controller.</p>
                <p>4 - COM port is not available.</p>
                <p>5 - An exception occurred.</p>
                <p>6 - Checksum error.</p>
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

- StatusRequest
- On or DeviceOn
- Off or DeviceOff
- Dim (1)
- Bright (1)
- AllUnitsOff (1)
- AllLightsOn (1)
- DefineDevice
- QueryDevices
- UpdateDevice
- DeleteDevice
- DefineProgram
- UpdateProgram
- DeleteDeviceProgram
- QueryDevicePrograms
- QueryDeviceProgram
- QueryAvailableDevices

(1) Not currently implemented

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
          "name": "X10-G15",
          "location": "",
          "type": "x10",
          "address": "G15",
          "selected": 0,
          "updatetime": "2019-06-06 11:46:58.570884"
        },
        {
          "id": 16,
          "name": "Window Seat Decorations",
          "location": "Breakfast Nook",
          "type": "x10",
          "address": "A4",
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
        "type": "x10",
        "address": "A2",
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
| device-type | x10, tplink, or meross | The type of device |
| device-address | X10, IP address, UUID | For an X10 device, the house-device-code (A1-L16). For a TPLink device, an IP address. For a Meross device, a UUID. |
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
| device-type | x10, tplink, or meross | The type of device |
| device-address | X10, IP address, UUID | For an X10 device, the house-device-code (A1-L16). For a TPLink device, an IP address. For a Meross device, a UUID. |
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
X10 modules cannot be discovered.

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
| x10 | house-device-code | e.g. A1, G16 |
| tplink | IP address | 192.168.1.78 |
| meross | UUID | 1907226943690825185048e1e901c0b7 |

# Client Examples

## Test Client

The test client application in
**testclient/ahps\_client.py** provides several
examples of sending commands to the server and receiving command
responses.

## AtHome Control

AtHome Control is an open source web server based application that works with
AtHomePowerlineServer. It can be found on GitHub at
<https://github.com/dhocker/athomefrb>.

# Appendix
## Device Identifiers
The devices supported by AtHome Control use significantly different
identifiers.
### X10 Modules
X10 modules are identified by an address consists of a letter (A to L) and a
number (from 1 to 16). Thus the range of X10 addresses is A1 to L16.
### TPLink/Kasa Devices
TPLink devices are identifier by their IP address. This address is
assigned to the device during configuration.
### Meross Devices
Meross devices are identified by a UUID. While the UUID looks like a
GUID, it does not seem to be a valid one. The UUID is 32 hex characters
without any hyphens. Example: 1907220924955625185048e1e901d533
# References

1.  [CM11A Protocol](http://jvde.us/info/CM11A_protocol.txt)
2.  [XTB-232](http://jvde.us//xtb/XTB-232_description.htm)
3.  [Raspberry Pi](http://www.raspberrypi.org/)
4.  [TPLink Python Library](https://github.com/GadgetReactor/pyHS100)
5.  [Meross Python Library](https://github.com/albertogeniola/MerossIot)
