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

logger = logging.getLogger("server")


class CommandHandler:
    call_sequence = 1

    # Error codes
    NotImplemented = 404
    UnhandledException = 405

    #######################################################################
    # Return an instance of the handler for a given command
    #
    # Complete list of CM11A functions from protocol spec
    # Function			            Binary Value
    # All Units Off			        0000
    # All Lights On			        0001
    # On				                0010
    # Off				                0011
    # Dim				                0100
    # Bright				            0101
    # All Lights Off		        0110
    # Extended Code			        0111
    # Hail Request			        1000
    # Hail Acknowledge	        1001
    # Pre-set Dim (1)		        1010
    # Pre-set Dim (2)		        1011
    # Extended Data Transfer		1100
    # Status On			            1101
    # Status Off			          1110
    # Status Request		        1111
    #
    # Most of these functions are supported as commands
    #
    def GetHandler(self, command):
        logger.info("GetHandler for command: %s", command)

        ci_command = command.lower()

        if ci_command == "loadtimers":
            handler = commands.LoadTimers.LoadTimers()
        elif ci_command == "loadactions":
            handler = commands.LoadActions.LoadActions()
        elif (ci_command == "deviceon") or (ci_command == "on"):
            handler = commands.DeviceOn.DeviceOn()
        elif (ci_command == "deviceoff") or (ci_command == "off"):
            handler = commands.DeviceOff.DeviceOff()
        elif ci_command == "allunitsoff":
            handler = commands.DeviceAllUnitsOff.DeviceAllUnitsOff()
        elif ci_command == "alllightson":
            handler = commands.DeviceAllLightsOn.DeviceAllLightsOn()
        elif ci_command == "dim":
            handler = commands.DeviceDim.DeviceDim()
        elif ci_command == "bright":
            handler = commands.DeviceBright.DeviceBright()
        elif ci_command == "alllightsoff":
            handler = commands.DeviceAllLightsOff.DeviceAllLightsOff()
        elif ci_command == "statusrequest":
            handler = commands.StatusRequest.StatusRequest()
        elif ci_command == "gettime":
            handler = commands.GetTime.GetTime()
        elif ci_command == "settime":
            handler = commands.SetTime.SetTime()
        elif ci_command == "getsundata":
            handler = commands.GetSunData.GetSunData()
        else:
            handler = None

        return handler

        #######################################################################

    # Execute the command specified by the incoming request
    def Execute(self, request):
        handler = self.GetHandler(request["request"])
        if handler is not None:
            response = handler.Execute(request)
            response['X10Response']['call-sequence'] = CommandHandler.call_sequence
        else:
            logger.error("No handler for command: %s", request["request"])
            response = CommandHandler.CreateErrorResponse(request["request"], CommandHandler.NotImplemented,
                                                          "Command is not recognized or implemented", "")

        CommandHandler.call_sequence += 1

        return response

    @classmethod
    def CreateErrorResponse(cls, request_command, result_code, error_msg, extra_data):
        response = commands.ServerCommand.ServerCommand.CreateResponse(request_command)
        r = response['X10Response']
        r['result-code'] = result_code
        r['error'] = error_msg
        r['call-sequence'] = cls.call_sequence
        r['data'] = extra_data
        return response
