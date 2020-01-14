#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Defines the interface for a server command handler.
# All command handlers should be derived from the ServerCommand class.
#

import datetime
import socket
import Version
from database.managed_devices import ManagedDevices
from drivers.device_driver_manager import DeviceDriverManager


class ServerCommand:

    def Execute(self, request):
        r = self.CreateResponse()
        r['result-code'] = 404
        r['error'] = "Command not recognized"
        r['date-time'] = str(datetime.datetime.now())
        r['message'] = "none"

        return r

    # Create an empty response instance
    @classmethod
    def CreateResponse(cls, command):
        r = {}
        r['request'] = command
        r['date-time'] = str(datetime.datetime.now())
        r['server'] = "{0}/AtHomePowerlineServer".format(socket.gethostname())
        r['server-version'] = Version.GetVersion()
        return r

    @classmethod
    def get_driver_for_id(cls, device_id):
        r = ManagedDevices.get_device_by_id(device_id)
        driver = DeviceDriverManager.get_driver(r["mfg"])
        return driver

    @classmethod
    def get_address_for_id(cls, device_id):
        r = ManagedDevices.get_device_by_id(device_id)
        return r["address"]

    @classmethod
    def get_device_for_id(cls, device_id):
        return ManagedDevices.get_device_by_id(device_id)

    @classmethod
    def parse_time_str(cls, time_string):
        if len(time_string) == 5:
            t = datetime.datetime.strptime(time_string, "%H:%M")
        elif len(time_string) == 8:
            t = datetime.datetime.strptime(time_string, "%H:%M:%S")
        else:
            t = datetime.datetime.strptime(time_string[-8:], "%H:%M:%S")
        return t
