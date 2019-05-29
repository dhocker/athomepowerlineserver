# -*- coding: utf-8 -*-
#
# Update a timer program - AtHomePowerlineServer
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
import timers.TimerStore
import database.Timers
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
        device_id = int(request["args"]["device-id"])
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
        database.Timers.Timers.update(id, name, device_id, day_mask,
                                           trigger_method, trigger_time, offset, randomize,
                                           randomize_amount,
                                           action, dimamount, security)

        # Update the timer program in the current list
        timers.TimerStore.TimerStore.UpdateTimer(id, name, device_id, day_mask,
                                                 trigger_method, trigger_time, offset, randomize,
                                                 randomize_amount,
                                                 action, dimamount, security=security)

        # Debugging...
        timers.TimerStore.TimerStore.DumpTimerProgramList()

        # Generate a successful response
        response = UpdateProgram.CreateResponse("UpdateProgram")
        r = response["X10Response"]

        # Return the timer program ID
        r['result-code'] = 0
        r['message'] = "Success"

        return response
