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
# SetTime
#

import commands.ServerCommand as ServerCommand


#######################################################################
# Command handler for GetTime command
# We always use the host machine time. Therefor, we don't do
# anything for this command
class SetTime(ServerCommand.ServerCommand):

    #######################################################################
    # Execute the GetTime command.
    def Execute(self, request):
        # Generate a successful response
        r = SetTime.CreateResponse(request["request"])

        # Success
        r['result-code'] = 0
        r['message'] = "Success"

        return r
