#
# AtHomPowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import ServerCommand
import timers.TimerStore
import datetime

#######################################################################
# Command handler for loading timer initiators
class LoadTimers(ServerCommand.ServerCommand):
  
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
      t = datetime.datetime.strptime(timer_program["ontime"], "%H:%M")
      #print "ontime:", timer_program["ontime"]
      print "ontime:", t, "minutes:", (t.hour * 60) + t.minute

      # Pull all of the timer program values out of the dict entry
      name = timer_program["name"]
      house_device_code = timer_program["housedevicecode"]
      day_mask = timer_program["daymask"]
      on_time = datetime.datetime.strptime(timer_program["ontime"], "%H:%M")
      off_time = datetime.datetime.strptime(timer_program["offtime"], "%H:%M")
      # Unclear what security is used for, but it is not part of the program
      security = False

      # Add the timer program to the current list
      timers.TimerStore.TimerStore.AppendTimer(name, house_device_code, day_mask, on_time, off_time, security)

    # Persist the new set of timer programs
    timers.TimerStore.TimerStore.SaveTimerProgramList()

    # Debugging...
    timers.TimerStore.TimerStore.DumpTimerProgramList()

    # TODO Update database with new programs.
    # TODO Put new timer programs into effect.
    timers.TimerStore.TimerStore.SaveTimerProgramList()
    
    # Generate a successful response
    response = LoadTimers.CreateResponse("LoadTimers")
    r = response["X10Response"]
    
    r['result-code'] = 0
    #r['error'] = "Command not implemented"
    r['message'] = "Success"

    return response