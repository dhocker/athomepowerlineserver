# -*- coding: utf-8 -*-
#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright © 2014, 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Device bright
#

import commands.ServerCommand as ServerCommand
import drivers.X10ControllerAdapter


#######################################################################
# Command handler for bright command
class DeviceBright(ServerCommand.ServerCommand):

    #######################################################################
    # Execute the "of" command.
    def Execute(self, request):
        result = drivers.X10ControllerAdapter.X10ControllerAdapter.DeviceBright(request["args"]["house-device-code"],
                                                                                int(request["args"]["bright-amount"]))

        # Generate a successful response
        r = DeviceBright.CreateResponse(request["request"])

        r['result-code'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastErrorCode()
        if result:
            # r['error'] = "Command not fully implemented"
            r['message'] = "Success"
        else:
            r['error'] = drivers.X10ControllerAdapter.X10ControllerAdapter.GetLastError()
            r['message'] = "Failure"

        return r
