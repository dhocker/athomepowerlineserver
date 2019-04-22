# AtHomePowerlineServer
Copyright © 2015, 2018 by Dave Hocker

## Overview

In the world of X10, most of the power line controllers like the CM11/CM11A have been around for years. The majority of the
sophisticated X10 management applications run on a PC or Mac and more or less use the power line controller as a relatively
“dumb” controller. There are a number of problems with the current configurations that the AtHomePowerlineServer aims to
address.

First, the AtHomePowerline server is designed to run on a light weight system (e.g. a Raspberry Pi) that can be run head-less
and fan-less. This is as opposed to a PC or Mac based solution. The small size of such a system like the Raspberry Pi allows
it to be positioned more freely (ideally, close to the breaker panel). And, a Raspberry Pi system can be assembled for
considerably less than a PC. While the server was designed to run on a lightweight system, it will run on any system that
supports Python 3.5 or later (including Windows).

Second, the communication mechanism to the AtHomePowerlineServer is TCP/IP (over Ethernet). A light weight system like the
Raspberry Pi supports many WiFi USB interfaces. This further improves the freedom of location for the X10 controller. In the
past, the distance between a PC and the X10 controller was gated by the need for physical wiring and RS-232 limitations. With
the AtHomePowerlineServer architecture, this limitation is effectively eliminated. 

Finally, the AtHomePowerlineServer application is open source. Anyone can fork it and build upon it. 

The AtHomePowerlineServer.pdf document describes: 

	* Installation 
	* Configuration 
	* Programming interface 

While the functionality of the AtHomePowerlineServer is designed with knowledge of the CM11/CM11A architecture, it does not
exactly match that architecture. The AtHomePowerlineServer is an abstraction of the capabilities of the CM11/CM11A. For
example, the AtHomePowerlineServer features timers and actions that are conceptually similar to the CM11/CM11A timer
initiators and macros, but they are not exactly alike.

## License

The server is licensed under the GNU General Public License v3 as published by the Free Software Foundation, Inc.. See the
LICENSE file for the full text of the license.

## Source Code

The full source is maintained on [GitHub](https://www.github.com/dhocker/athomepowerlineserver).

## Build Environment

AtHomePowerlineServer was originally written in Python 2.7, but has since been converted 
to Python 3.5+. Use virtualenv and virtualenvwrapper to create a working virtual environment. 
The requirements.txt file can be used 
with pip to create the required virtual environment with all dependencies. Complete details
for installation, setup and configuration can be found in the AtHomePowerlineServer.pdf document.

AtHomePowerlineServer was developed using PyCharm CE. PyCharm CE is highly recommended. However, a good 
text editor of your choice is all that is really required.

## Documentation

See the AtHomePowerlineServer.pdf document. 
