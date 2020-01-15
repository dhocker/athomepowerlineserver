# -*- coding: utf-8 -*-
#
# Update a timer program - AtHomePowerlineServer
# Copyright © 2019, 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
import database.programs
import datetime
import logging

logger = logging.getLogger("server")


class UpdateProgram(ServerCommand):
    """
    Command handler for defining a new timer program
    """

    def Execute(self, request):
        """
        # Execute the load timers command. The new timer program is
        # inserted into the Timers table and appended to the
        # active timer list.
        :param request:
        :return:
        """

        # Pull all of the timer program values out of the dict entry
        id = int(request["args"]["id"])
        name = request["args"]["name"]
        day_mask = request["args"]["day-mask"]
        trigger_method = request["args"]["trigger-method"]
        trigger_time = self.parse_time_str(request["args"]["time"])
        offset = int(request["args"]["offset"])
        action = request["args"]["command"]
        randomize = True if int(request["args"]["randomize"]) else False
        randomize_amount = int(request["args"]["randomize-amount"])
        dimamount = int(request["args"]["dimamount"])
        # Unclear what security is used for, but it is not part of the program
        security = False

        # Insert program into Timers table
        database.programs.Programs.update(id, name, day_mask,
                                          trigger_method, trigger_time, offset, randomize,
                                          randomize_amount,
                                          action, dimamount, security)

        # Generate a successful response
        r = UpdateProgram.CreateResponse("UpdateProgram")

        # Return the timer program ID
        r['result-code'] = 0
        r['id'] = id
        r['message'] = "Success"

        return r
