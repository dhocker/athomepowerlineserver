# -*- coding: utf-8 -*-
#
# Define a timer program - AtHomePowerlineServer
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
import database.programs
import datetime
import logging

logger = logging.getLogger("server")


class DefineProgram(ServerCommand):
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
        # Historical Note
        # The CM11A X10 controller expects time in terms of the number of minutes
        # since midnight of the current day. Here, we play with converting
        # the on/off times to that format.
        # Note: In this implementation there is not real reason to limit timers
        # to the HH:MM format. We are never going to store these in an X10 controller.
        # In this implementation the server IS the X10 controller. The hardware X10 controller
        # is just a down-stream component used to transmit immediate X10 signals.

        # Pull all of the timer program values out of the dict entry
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
        id = database.programs.Programs.insert(name, day_mask,
                                               trigger_method, trigger_time, offset, randomize,
                                               randomize_amount,
                                               action, dimamount, security)

        # Add the timer program to the current list
        timers.TimerStore.TimerStore.AppendTimer(id, name, day_mask,
                                                 trigger_method, trigger_time, offset, randomize,
                                                 randomize_amount,
                                                 action, dimamount, security=security)

        # Debugging...
        timers.TimerStore.TimerStore.DumpTimerProgramList()

        # Generate a successful response
        r = DefineProgram.CreateResponse("DefineProgram")

        # Return the timer program ID
        r['result-code'] = 0
        r['id'] = id
        r['message'] = "Success"

        return r
