# AtHomePowerlineServer

Copyright © 2014, 2021 Dave Hocker (<AtHomeX10@gmail.com>)

# Overview
**Notice:
Version 2021.1.0.3 at tag v2021.1.0.3 is the last version to
support X10. Versions after that only support WiFi based
plugs and bulbs.**

The original version of AtHomePowerlineServer (AHPS) was written for X10 
controllers and modules. However, time has marched on and today the world
is dominated by WiFi based controllers, switches and bulbs.

AHPS was designed to run on a light weight
system (e.g. a Raspberry Pi v1, v2, v3, v4 or Zero W) that can be run
head-less and fan-less. This is as opposed to a PC or Mac based
solution. 
A Raspberry Pi system can be assembled for considerably less than a
PC. While the server was designed to run on a lightweight system, it
will run on any system that supports Python 3.5 or later (including Linux,
Windows and macOS).

The communication mechanism to AHPS is
TCP/IP. A light weight system like the Raspberry Pi
supports many WiFi USB interfaces and the later versions of the RPi have
integrated WiFi interfaces (e.g. RPi 3, RPi 4, RPi Zero W).
This further improves the freedom of
location.

AHPS provides support for a number of TPLink/Kasa
WiFi devices and Meross WiFi devices. This support covers a wide variety
of switches and bulbs.

Finally, the AHPS application is open source. Anyone
can fork it and build upon it.

The remainder of this document covers these topics.

  - [Supported devices](#supporteddevices)
  - [Installation](#installation)
  - [Configuration File](#configurationfile)
  - [Client Web App](#athomecontrolwebapp)
  - [Programming API](#programmingapi)

The AHPS is an abstraction of the
capabilities of the typical switch. 
It has devices and timer programs. A device is a TPLink/Kasa WiFi device or a Meross WiFi device.
A timer program defines a trigger and a
command/action to be executed when the trigger fires. Commands are logcial
actions like On and Off. Essentially, AHPS is independent
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
Many thanks to the contributors behind these packages.

[TPLink Python Library](https://github.com/python-kasa/python-kasa)

[Meross Python Library](https://github.com/albertogeniola/MerossIot) by Alberto Geniola.

# Supported Devices

## TPLink/Kasa WiFi Modules
### [Smart Plugs](https://www.kasasmart.com/us/products/smart-plugs)
* HS100
* HS103
* HS105
* HS107
* HS110

###[Smart Switches](https://www.kasasmart.com/us/products/smart-switches)
* HS210 (3-way)

### [Smart Bulbs](https://www.kasasmart.com/us/products/smart-lighting)
* LB130

## Meross Devices
[WiFi Devices](https://www.meross.com/)

### WiFi Plugs
* MSS110
* MSS210 (untested)
* MSS620 (channels 0, 1, 2)

### WiFi Bulbs
* MSL120, MSL120d, MSL120j (color supported)

### References
* [https://github.com/albertogeniola/MerossIot](https://github.com/albertogeniola/MerossIot)
  * The original Meross package
* [https://github.com/woder/MerossIot](https://github.com/woder/MerossIot)
  * A fork of the original package at 0.2.x.x. 
  * This version works significantly different from the original at version 0.4.x.x

# Devices to be Researched
Devices listed here are not currently supported. They need to be researched
to determine if they can be supported.

## Wyze
Wyze currently makes 3 WiFi devices: a bulb, a plug and an outdoor plug. Wyze does not seem to have 
an API, but there is some activity on GitHub.

[Wyze Web Site](https://wyze.com)

[Wyze Bulb](https://wyze.com/wyze-bulb.html)

[Wyze Bulb Python Support on GitHub](https://github.com/JoshuaMulliken/ha-wyzeapi)

[Wyze Plug](https://wyze.com/wyze-plug.html)

[Wyze Outdoor Plug](https://wyze.com/wyze-plug-outdoor.html)

[Wyze Python Client SDK](https://github.com/shauntarves/wyze-sdk)

# Installation

## Basic Steps for Raspberry Pi OS

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

Clone the repository from GitHub. Under Raspberry Pi OS the
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

Copy the file AtHomePowerlineServer.example.conf to
AtHomePowerlineServer.conf.

Edit the AtHomePowerlineServer.conf configuration file as needed.
You will need to change the
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
AHPS will create the database when needed.

## Files and Their Location

There are two key files:

  - AtHomePowerlineServer.conf – the configuration file
  - AtHomePowerlineServer.sqlite3 – the database file

These files are kept in OS dependent locations. AtHomePowerlineServer
automatically creates the database file (if it does not exist), so there
is little to worry about there.

### Linux Based Systems

On Linux based systems like Raspberry Pi OS, the key files are
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
            <td>The city where the installation is located. 
            Used for accurately calculating the sunset and sunrise 
            (using the astral package). If specified, latitude and longitude override
            the astral database values. If city is omitted, latitude and longitude are 
            required.
            </td>
        </tr>
        <tr class="even">
            <td>Latitude</td>
            <td>The latitude of installation. Required if city is omitted.</td>
        </tr>
        <tr class="odd">
            <td>Longitude</td>
            <td>The longitude of the installation. Required if city is omitted.</td>
        </tr>
        <tr class="even">
            <td>MerossEmail</td>
            <td>The email you used to set up your Meross account.</td>
        </tr>
        <tr class="odd">
            <td>Meross Password</td>
            <td>The password to your Meross account. See notes below discussing security.</td>
        </tr>
        <tr class="even">
            <td>Meross Settings</td>
            <td>
                <p>command_timeout (in seconds)</br>
                api_base_url (for Meross cloud server: https://iotx-us.meross.com)</p> 
            </td>
        </tr>
        <tr class="odd">
            <td>PyKasaDiscoverTarget</td>
            <td>The IP address to be used as the target of device discovery</td>
        </tr>
        <tr class="even">
            <td>PyKasaRequestWaitTime</td>
            <td>The time (in seconds) to wait for a request to complete</td>
        </tr>
    </tbody>
</table>

### Example
```json
{
  "Configuration":
  {
    "Port": 9999,
    "LogFile": "AtHomePowerlineServer.log",
    "LogConsole": "True",
    "LogLevel": "DEBUG",
    "DatabasePath": "",
    "City": "Houston",
    "Latitude": "29.9947",
    "Longitude": "-95.6675",
    "MerossEmail": "your Meross email",
    "MerossPassword": "your Meross account password",
    "MerossIot": {
        "command_timeout": 2.0,
        "api_base_url": "https://iotx-us.meross.com"
        },
    "PyKasaDiscoverTarget": "192.168.1.255",
    "PyKasaRequestWaitTime": 5.0
   }
}
```

### Notes
For api_base_url use https://iotx-us.meross.com in the US and https://iotx-eu.meross.com 
in Europe.

If you are using Meross devices, you should set the permissions of the
configuration file to limit access. At a minimum, you should disallow
any access by "everyone". Under Linux, you should at least chmod the
file to permissions to something like 640 or even the more restrictive 600.
Under Windows, you should remove "Everyone" from the file's permissions.

If you are using the [At Home Control](https://github.com/dhocker/athomefrb)
web client, you will find that it only supports
TPLink and Meross device drivers. The TPLink driver will work with most TPLink/Kasa devices and
the Meross driver will work with Meross WiFi plugs and bulbs.

## Running the Server

### Raspberry Pi OS

#### As an Application

Start the server:

```bash
sudo python AtHomePowerlineServer.py
```

#### As a Daemon

This technique will set up AtHomePowerlineServer so that it
automatically starts when Raspberry Pi OS boots up.

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


# AtHome Control Web App

AtHome Control (AthomeFRB) is an open source web server based application that works with
AHPS. It can be found on GitHub at
<https://github.com/dhocker/athomefrb>.

Using AthomeFRB you can:

- Add devices to the system
- Monitor all of the devices in the system
- Set up timer programs to control devices
- Assign timer programs to devices (one timer program can be applied to many devices)
- Place related devices into a group (e.g. devices in a room)

# Programming API
The programming API is described in [readme-api.md](https://github.com/dhocker/athomepowerlineserver/blob/master/readme-api.md)

# Appendix
## Device Identifiers
The devices supported by AtHome Control use significantly different
identifiers.
### TPLink/Kasa Devices
TPLink devices are identifier by their IP address. This address is
assigned to the device during configuration via the Kasa mobile app.
### Meross Devices
Meross devices are identified by a UUID. While the UUID looks like a
GUID, it does not seem to be a valid one. The UUID is 32 hex characters
without any hyphens. Example: 1907220924955625185048e1e901d533
# References

1.  [Raspberry Pi](http://www.raspberrypi.org/)
1.  [TPLink Python Library](https://github.com/python-kasa/python-kasa)
1.  [Meross Python Library](https://github.com/albertogeniola/MerossIot)
1.  [Programming API](https://github.com/dhocker/athomepowerlineserver/blob/master/readme-api.md)
