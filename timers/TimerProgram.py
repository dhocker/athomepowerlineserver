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

#
# Timer program - represents the equivalent of a timer initiator
#
# The program is limited to turning a device on then off
#

#######################################################################

import datetime
import database.sun_table
import logging

logger = logging.getLogger("server")

class TimerProgram:

  #######################################################################
  # Instance constructor
  def __init__(self, name, house_device_code, day_mask, start_trigger_method, start_time, start_offset, \
               stop_trigger_method, stop_time, stop_offset, \
               start_action, stop_action, security):
    self.Name = name
    self.HouseDeviceCode = house_device_code
    self.DayMask = day_mask
    self.StartTriggerMethod = start_trigger_method
    self.StartTime = start_time
    self.StartOffset = start_offset
    self.StopTriggerMethod = stop_trigger_method
    self.StopTime = stop_time
    self.StopOffset = stop_offset
    self.StartAction = start_action
    self.StopAction = stop_action
    self.Security = security

    # These are used to monitor the timer events
    self.StartEventRun = False
    self.StopEventRun = False

  def __str__(self):
    """
    Custom str implementation
    """
    s = "{0} {1} {2} ".format(self.Name, self.HouseDeviceCode, self.DayMask)

    if self.StartTriggerMethod == "clock-time":
      s = s + "Start: {0} {1} ".format(self.StartTriggerMethod, self.StartTime)
    else:
      s = s + "Start: {0} {1} ".format(self.StartTriggerMethod, self.StartOffset)

    if self.StopTriggerMethod == "clock-time":
      s = s + "Stop: {0} {1}".format(self.StopTriggerMethod, self.StopTime)
    else:
      s = s + "Stop: {0} {1}".format(self.StopTriggerMethod, self.StopOffset)

    return s


  def DecodeDayMask(self, day_mask):
    """
    Decode day mask format into an array where [0] is Monday
    and [6] is Sunday.
    Day mask format: MTWTFSS (Monday through Sunday)
    Event days have the letter while non-event days have a '-' or '.'
    """
    # Sunday through to Saturday
    effective_days = [False, False, False, False, False, False, False]

    for dx in range(0, 7):
      if (day_mask[dx] != '-') and (day_mask[dx] != '.'):
        effective_days[dx] = True
    
    return effective_days

  # TODO There's probably some refactoring to be done here

  def IsStartEventTriggered(self, time_to_test):
    """
    Test the program against the given time to see if the start event has occurred.
    """

    # We use the time part of the datetime to mean the time TODAY.
    now = datetime.datetime.now()

    # time without seconds
    now_dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)

    # Factory testing based on trigger method
    if self.StartTriggerMethod == "clock-time":
      today_starttime = datetime.datetime(now.year, now.month, now.day, self.StartTime.hour, self.StartTime.minute, self.StartTime.second)
      return today_starttime == now_dt
    elif self.StartTriggerMethod == "sunset":
      #logger.debug("Testing start sunset trigger")
      sunset = database.sun_table.get_sunset(datetime.date(now_dt.year, now_dt.month, now_dt.day))
      offset_sunset = sunset + datetime.timedelta(minutes=self.StartOffset)
      return now_dt == offset_sunset
    elif self.StartTriggerMethod == "sunrise":
      #logger.debug("Testing start sunrise trigger")
      sunrise = database.sun_table.get_sunrise(datetime.date(now_dt.year, now_dt.month, now_dt.day))
      offset_sunrise = sunrise + datetime.timedelta(minutes=self.StartOffset)
      return now_dt == offset_sunrise

    return False


  def IsStopEventTriggered(self, time_to_test):
    """
    Test the program against the given time to see if the stop event has occurred.
    """

    # We use the time part of the datetime to mean the time TODAY.
    now = datetime.datetime.now()

    # time without seconds
    now_dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)

    # Factory testing based on trigger method
    if self.StopTriggerMethod == "clock-time":
      # Stop time using today's date
      today_stoptime = datetime.datetime(now.year, now.month, now.day, self.StopTime.hour, self.StopTime.minute, self.StopTime.second)
      return today_stoptime == now_dt
    elif self.StopTriggerMethod == "sunset":
      #logger.debug("Testing stop sunset trigger")
      sunset = database.sun_table.get_sunset(datetime.date(now_dt.year, now_dt.month, now_dt.day))
      offset_sunset = sunset + datetime.timedelta(minutes=self.StopOffset)
      return now_dt == offset_sunset
    elif self.StopTriggerMethod == "sunrise":
      #logger.debug("Testing stop sunrise trigger")
      sunrise = database.sun_table.get_sunrise(datetime.date(now_dt.year, now_dt.month, now_dt.day))
      offset_sunrise = sunrise + datetime.timedelta(minutes=self.StopOffset)
      return now_dt == offset_sunrise

    return False
