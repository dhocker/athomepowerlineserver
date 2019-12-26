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

import json
import datetime
import logging
import commands.ServerCommand
import commands.LoadTimers
import commands.LoadActions
import commands.ServerCommand
import commands.StatusRequest
import commands.DeviceOn
import commands.DeviceOff
import commands.DeviceDim
import commands.DeviceBright
import commands.DeviceAllUnitsOff
import commands.DeviceAllLightsOff
import commands.DeviceAllLightsOn
import commands.GetTime
import commands.SetTime
import commands.GetSunData
import commands.define_device
import commands.query_devices
import commands.update_device
import commands.define_program
import commands.update_program
import commands.query_device_programs
import commands.query_device_program
import commands.delete_device
import commands.delete_device_program
import commands.all_selected_devices_on
import commands.all_selected_devices_off
import commands.query_available_devices

logger = logging.getLogger("server")


class CommandHandler:
    call_sequence = 1

    # Error codes
    NotImplemented = 404
    UnhandledException = 405

    COMMAND_HANDLER_LIST = {
        "deviceon": commands.DeviceOn.DeviceOn,
        "on": commands.DeviceOn.DeviceOn,
        "deviceoff": commands.DeviceOff.DeviceOff,
        "off": commands.DeviceOff.DeviceOff,
        "allunitsoff": commands.DeviceAllUnitsOff.DeviceAllUnitsOff,
        "alllightson": commands.DeviceAllLightsOn.DeviceAllLightsOn,
        "dim": commands.DeviceDim.DeviceDim,
        "bright": commands.DeviceBright.DeviceBright,
        "statusrequest": commands.StatusRequest.StatusRequest,
        "gettime": commands.GetTime.GetTime,
        "settime": commands.SetTime.SetTime,
        "getsundata": commands.GetSunData.GetSunData,
        "definedevice": commands.define_device.DefineDevice,
        "querydevices": commands.query_devices.QueryDevices,
        "queryavailabledevices": commands.query_available_devices.QueryAvailableDevices,
        "updatedevice": commands.update_device.UpdateDevice,
        "deletedevice": commands.delete_device.DeleteDevice,
        "defineprogram": commands.define_program.DefineProgram,
        "updateprogram": commands.update_program.UpdateProgram,
        "deletedeviceprogram": commands.delete_device_program.DeleteDeviceProgram,
        "querydeviceprograms": commands.query_device_programs.QueryDevicePrograms,
        "querydeviceprogram": commands.query_device_program.QueryDeviceProgram,
        "allselecteddeviceson": commands.all_selected_devices_on.AllSelectedDevicesOn,
        "allselecteddevicesoff": commands.all_selected_devices_off.AllSelectedDevicesOff
    }

    def GetHandler(self, command):
        """
        Return an instance of the handler for a given command
        :param command: API command as a string
        :return: Instance of class that executes the command
        """
        logger.info("GetHandler for command: %s", command)

        ci_command = command.lower()
        if ci_command in self.COMMAND_HANDLER_LIST.keys():
            handler = self.COMMAND_HANDLER_LIST[ci_command]()
        else:
            handler = None

        return handler

        #######################################################################

    # Execute the command specified by the incoming request
    def Execute(self, request):
        handler = self.GetHandler(request["request"])
        if handler is not None:
            response = handler.Execute(request)
            response['call-sequence'] = CommandHandler.call_sequence
        else:
            logger.error("No handler for command: %s", request["request"])
            response = CommandHandler.CreateErrorResponse(request["request"], CommandHandler.NotImplemented,
                                                          "Command is not recognized or implemented", "")

        CommandHandler.call_sequence += 1

        return response

    @classmethod
    def CreateErrorResponse(cls, request_command, result_code, error_msg, extra_data):
        r = commands.ServerCommand.ServerCommand.CreateResponse(request_command)
        r['result-code'] = result_code
        r['error'] = error_msg
        r['call-sequence'] = cls.call_sequence
        r['data'] = extra_data
        return r
