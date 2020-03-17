#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright © 2014, 2020  Dave Hocker
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
from http import HTTPStatus
import Version
from database.managed_devices import ManagedDevices
from drivers.device_driver_manager import DeviceDriverManager
import logging

logger = logging.getLogger("server")


class ServerCommand:
    # Error codes
    SUCCESS = 0
    OK = HTTPStatus.OK
    BAD_REQUEST = HTTPStatus.BAD_REQUEST
    COMMAND_NOT_FOUND = HTTPStatus.NOT_FOUND
    SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR
    NOT_IMPLEMENTED = HTTPStatus.NOT_IMPLEMENTED
    # Messages
    MSG_SUCCESS = "Success"
    MSG_BAD_REQUEST = "Incomplete/invalid request"

    def Execute(self, request):
        r = self.CreateResponse()
        r['result-code'] = ServerCommand.COMMAND_NOT_FOUND
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
    def get_driver_for_mfg(cls, device_mfg):
        """
        Return a device driver instance for a given device mfg/type
        :param device_mfg:
        :return:
        """
        driver = DeviceDriverManager.get_driver(device_mfg)
        return driver

    @classmethod
    def get_driver_for_id(cls, device_id):
        """
        Return a device driver instance for a given device ID
        :param device_id:
        :return:
        """
        device = ServerCommand.get_device_for_id(device_id)
        if device is not None:
            driver = DeviceDriverManager.get_driver(device["mfg"])
        else:
            driver = None
        return driver

    @classmethod
    def get_address_for_id(cls, device_id):
        """
        Return the address/UUID for a given device ID
        :param device_id:
        :return:
        """
        r = ServerCommand.get_device_for_id(device_id)
        if r is None:
            return None
        return r["address"]

    @classmethod
    def get_device_for_id(cls, device_id):
        """
        Get the device record for a given device ID
        :param device_id:
        :return:
        """
        md = ManagedDevices()
        device = md.get_device_by_id(device_id)
        if device is None:
            logger.error("No device record for device %d", device_id)
            logger.error(md.last_error)
        return device

    @classmethod
    def parse_time_str(cls, time_string):
        if len(time_string) == 5:
            t = datetime.datetime.strptime(time_string, "%H:%M")
        elif len(time_string) == 8:
            t = datetime.datetime.strptime(time_string, "%H:%M:%S")
        else:
            t = datetime.datetime.strptime(time_string[-8:], "%H:%M:%S")
        return t
