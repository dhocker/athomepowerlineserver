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
                        <ul>
                            <li>X10-appliance</li>
                            <li>X10-lamp</li>
                        </ul>
                        <li>TPLink</li>
                        <ul>
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
                        </ul>
                        <li>Meross</li>
                        <ul>
                            <li>MSS110</li>
                            <li>MSL120</li>
                            <li>MSS620</li>
                        </ul>
                    </ul>
                    See example below.
                </p>
            </td>
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
