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

import commands.ServerCommand
import timers.TimerStore
import datetime
import logging

logger = logging.getLogger("server")


#######################################################################
# TODO Remove
# Command handler for loading timer initiators
class LoadTimers(commands.ServerCommand.ServerCommand):

    #######################################################################
    # Execute the load timers command.
    # We replace the current set of timer programs/initiators with
    # whatever is in the request payload.
    def Execute(self, request):
        # Reset the timer program list to empty
        timers.TimerStore.TimerStore.ClearTimerProgramList()

        # The CM11A X10 controller expects time in terms of the number of minutes
        # since midnight of the current day. Here, we play with converting
        # the on/off times to that format.
        # Note: In this implementation there is not real reason to limit timers
        # to the HH:MM format. We are never going to store these in an X10 controller.
        # In this implementation the server IS the X10 controller. The hardware X10 controller
        # is just a down-stream component used to transmit immediate X10 signals.
        for timer_program in request["args"]["programs"]:
            t = datetime.datetime.strptime(timer_program["start-time"], "%H:%M")
            # print "start-time:", timer_program["start-time"]
            # logging("start-time: %s minutes: %s", t, (t.hour * 60) + t.minute

            # Pull all of the timer program values out of the dict entry
            name = timer_program["name"]
            device_id = timer_program["device-id"]
            day_mask = timer_program["day-mask"]
            start_trigger_method = timer_program["start-trigger-method"]
            start_time = datetime.datetime.strptime(timer_program["start-time"], "%H:%M")
            start_offset = int(timer_program["start-time-offset"])
            stop_trigger_method = timer_program["stop-trigger-method"]
            stop_time = datetime.datetime.strptime(timer_program["stop-time"], "%H:%M")
            stop_offset = int(timer_program["stop-time-offset"])
            start_action = timer_program["start-action"]
            stop_action = timer_program["stop-action"]
            start_randomize = True if int(timer_program["start-randomize"]) else False
            start_randomize_amount = int(timer_program["start-randomize-amount"])
            stop_randomize = True if int(timer_program["stop-randomize"]) else False
            stop_randomize_amount = int(timer_program["stop-randomize-amount"])
            # Unclear what security is used for, but it is not part of the program
            security = False

            # Add the timer program to the current list
            timers.TimerStore.TimerStore.AppendTimer(name, device_id, day_mask, \
                                                     start_trigger_method, start_time, start_offset, start_randomize,
                                                     start_randomize_amount, \
                                                     stop_trigger_method, stop_time, stop_offset, stop_randomize,
                                                     stop_randomize_amount, \
                                                     start_action, stop_action, security=security)

        # Debugging...
        timers.TimerStore.TimerStore.DumpTimerProgramList()

        # Update database with new programs.
        # Put new timer programs into effect.
        timers.TimerStore.TimerStore.SaveTimerProgramList()

        # Generate a successful response
        r = LoadTimers.CreateResponse("LoadTimers")

        r['result-code'] = 0
        # r['error'] = "Command not implemented"
        r['message'] = "Success"

        return r
