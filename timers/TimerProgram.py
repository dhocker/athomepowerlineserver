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

#######################################################################

import datetime
import random
from helpers.TimeZone import TimeZone
from helpers.sun_data import get_sunrise, get_sunset
import logging

logger = logging.getLogger("server")

class TimerProgram:

  #######################################################################
  # Instance constructor
  def __init__(self, name, house_device_code, day_mask,
               start_trigger_method, start_time, start_offset, start_randomize, start_randomize_amount,
               stop_trigger_method, stop_time, stop_offset, stop_randomize, stop_randomize_amount,
               start_action, stop_action, security):
    self.Name = name
    self.HouseDeviceCode = house_device_code
    self.DayMask = day_mask
    self.StartTriggerMethod = start_trigger_method
    self.StartTime = start_time
    self.StartOffset = start_offset
    self.StartRandomize = start_randomize
    self.StartRandomizeAmount = start_randomize_amount
    self.StopTriggerMethod = stop_trigger_method
    self.StopTime = stop_time
    self.StopOffset = stop_offset
    self.StopRandomize = stop_randomize
    self.StopRandomizeAmount = stop_randomize_amount
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
    s = s + "Randomize: {0} {1} ".format(self.StartRandomize, self.StartRandomizeAmount)

    if self.StopTriggerMethod == "clock-time":
      s = s + "Stop: {0} {1} ".format(self.StopTriggerMethod, self.StopTime)
    else:
      s = s + "Stop: {0} {1} ".format(self.StopTriggerMethod, self.StopOffset)
    s = s + "Randomize: {0} {1}".format(self.StopRandomize, self.StopRandomizeAmount)

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

  def IsStartEventTriggered(self):
    """
    Test the program against the given time to see if the start event has occurred.
    """

    # We use the time part of the datetime to mean the time TODAY.
    now = datetime.datetime.now()

    # time without seconds
    now_dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0, tzinfo=TimeZone())

    # Randomized amount
    randomized_amount = 0
    if self.StartRandomize:
      randomized_amount = self.GetRandomizedAmount(self.StartRandomizeAmount)
    logger.debug("Start randomize amount: %s", randomized_amount)

    # Factory testing based on trigger method
    if self.StartTriggerMethod == "clock-time":
      today_starttime = datetime.datetime(now.year, now.month, now.day, self.StartTime.hour,
                                          self.StartTime.minute, self.StartTime.second, tzinfo=TimeZone())
      today_starttime = today_starttime + datetime.timedelta(minutes=(self.StartOffset + randomized_amount))
      return today_starttime == now_dt
    elif self.StartTriggerMethod == "sunset":
      #logger.debug("Testing start sunset trigger")
      sunset = get_sunset(now_dt)
      offset_sunset = sunset + datetime.timedelta(minutes=(self.StartOffset + randomized_amount))
      return now_dt == offset_sunset
    elif self.StartTriggerMethod == "sunrise":
      #logger.debug("Testing start sunrise trigger")
      sunrise = get_sunrise(now_dt)
      offset_sunrise = sunrise + datetime.timedelta(minutes=(self.StartOffset + randomized_amount))
      return now_dt == offset_sunrise

    # "none" falls to here
    return False


  def IsStopEventTriggered(self):
    """
    Test the program against the given time to see if the stop event has occurred.
    """

    # We use the time part of the datetime to mean the time TODAY.
    now = datetime.datetime.now()

    # Randomized amount
    randomized_amount = 0
    if self.StopRandomize:
      randomized_amount = self.GetRandomizedAmount(self.StopRandomizeAmount)
    logger.debug("Stop randomize amount: %s", randomized_amount)

    # time without seconds
    now_dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0, tzinfo=TimeZone())

    # Factory testing based on trigger method
    if self.StopTriggerMethod == "clock-time":
      # Stop time using today's date
      today_stoptime = datetime.datetime(now.year, now.month, now.day, self.StopTime.hour,
                                         self.StopTime.minute, self.StopTime.second, tzinfo=TimeZone())
      today_stoptime = today_stoptime + datetime.timedelta(minutes=(self.StopOffset + randomized_amount))
      #logger.debug("Target stop time: %s", today_stoptime)
      return today_stoptime == now_dt
    elif self.StopTriggerMethod == "sunset":
      #logger.debug("Testing stop sunset trigger")
      sunset = get_sunset(now_dt)
      offset_sunset = sunset + datetime.timedelta(minutes=(self.StopOffset + randomized_amount))
      return now_dt == offset_sunset
    elif self.StopTriggerMethod == "sunrise":
      #logger.debug("Testing stop sunrise trigger")
      sunrise = get_sunrise(now_dt)
      offset_sunrise = sunrise + datetime.timedelta(minutes=(self.StopOffset + randomized_amount))
      logger.debug("Testing stop sunrise trigger: {0} == {1}".format(now_dt, offset_sunrise))
      return now_dt == offset_sunrise

    # "none" falls to here
    return False


  def GetRandomizedAmount(self, randomize_amount):
    """
    For today's date, calculate the integer randomized amount r where
    -randomize_amount <= int(r) <= randomize_amount
    """

    # Today's randomization factor
    rf = self.GetRandomFactor()

    # Round randomized value to a whole integer
    # Return the result as an integer
    return int(round(rf * float(randomize_amount)))


  def GetRandomFactor(self):
    """
    Returns a floating point randomization factor in the range -1.0 <= f <= 1.0
    """

    # We want to use today's date as the seed (just the date).
    # This will allow us to reproduce a random factor for a given date, while
    # allowing the factor to vary over a range of dates.
    now = datetime.datetime.now()
    now_date = datetime.date(now.year, now.month, now.day)
    random.seed(now_date)

    # We'll try to inject a little more controlled randomness by using today's
    # day as an additional factor.
    f = 1.0
    for i in range(0, now_date.day):
      f = random.uniform(-1.0, 1.0)

    return f