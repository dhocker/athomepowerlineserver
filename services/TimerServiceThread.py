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
# TimerService thread
#

import threading
import time
import datetime
import logging
import timers.TimerStore
import timers.TimerProgram
import database.Actions
import TimerActions

########################################################################
# The timer service thread periodically examines the list of timer programs.
# When a timer event expires, it transmits the appropriate X10 function.
class TimerServiceThread(threading.Thread):

  ########################################################################
  # Constructor
  def __init__(self, thread_id, name):
    threading.Thread.__init__(self)
    self.thread_id = thread_id
    self.name = name
    self.terminate_signal = False

  ########################################################################
  # Called by threading on the new thread
  def run(self):
    # logging.info("Timer service running")

    # Line up timing to the minute
    time_count = datetime.datetime.now().second
    # Check the terminate signal every second
    while not self.terminate_signal:
      time.sleep(1.0)
      time_count += 1
      # Every minute run the program checks
      if time_count >= 60:
        # Maintain top of the minute alignment
        time_count = datetime.datetime.now().second
        # run checks
        logging.info("Timer checks")
        self.RunTimerPrograms()

  ########################################################################
  # Terminate the timer service thread
  def Terminate(self):
    self.terminate_signal = True
    # wait for service thread to exit - could be a while
    logging.info("Waiting for timer service to stop...this could take a few seconds")
    self.join()
    logging.info("Timer service stopped")

  ########################################################################
  # Run timer programs that have reached their trigger time
  def RunTimerPrograms(self):
    tp_list = timers.TimerStore.TimerStore.AcquireTimerProgramList()

    try:
      for tp in tp_list:
        self.RunTimerProgram(tp)
    finally:
      timers.TimerStore.TimerStore.ReleaseTimerProgramList()
  
  ########################################################################
  # Run a single timer program
  def RunTimerProgram(self, tp):
    # The date in a timer program's on/off time has no meaning.
    # We use the time part of the datetime to mean the time TODAY.
    now = datetime.datetime.now()
    # On/Off times for TODAY
    today_starttime = datetime.datetime(now.year, now.month, now.day, tp.StartTime.hour, tp.StartTime.minute, tp.StartTime.second)
    today_stoptime = datetime.datetime(now.year, now.month, now.day, tp.StopTime.hour, tp.StopTime.minute, tp.StopTime.second)

    # logging.debug("%s %s", tp.HouseDeviceCode, tp.DecodeDayMask(tp.DayMask))

    # TODO Answer question about persisting event status in database (and resetting status at well defined times)

    # time without seconds
    now_dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)

    # Only if the current day is enabled...
    if TimerServiceThread.IsDayOfWeekEnabled(now, tp.DayMask):
      # we consider the event triggered if the current date/time in hours and minutes matches the event time
      logging.info("Start: %s %s", tp.StartTime, now_dt)
      logging.info("Stop: %s %s", tp.StopTime, now_dt)

      # Start event check
      if (not tp.StartEventRun) and (today_starttime == now_dt):
        # Start event triggered
        tp.StartEventRun = True
        logging.info("Start event triggered: %s %s %s %s", tp.Name, tp.DayMask, tp.StartTime, tp.StartAction)
        self.RunTimerAction(tp.StartAction, tp.HouseDeviceCode)

      # Stop event check
      if (not tp.StopEventRun) and (today_stoptime == now_dt):
        # Stop event triggered
        tp.StopEventRun = True
        logging.info("Stop event triggered: %s %s %s %s", tp.Name, tp.DayMask, tp.StopTime, tp.StopAction)
        self.RunTimerAction(tp.StopAction, tp.HouseDeviceCode)
    else:
      logging.info("Program is not enabled for the current weekday: %s", tp.Name)

  ########################################################################
  # Run an action
  def RunTimerAction(self, name, house_device_code):
    rset = database.Actions.Actions.GetByName(name)
    if rset is not None:
      #print type(rset)
      #print rset
      # TODO We want a factory here, one that looks up the action and returns an action handler
      logging.info("Executing action: %s %s", rset["command"], house_device_code)
      action = TimerActions.GetAction(rset["command"])
      action(house_device_code, rset["dimamount"], rset["args"])
    else:
      logging.info("No Actions table record was found for: %s", name)

  ########################################################################
  # Test a date to see if its weekday is enabled
  @classmethod
  def IsDayOfWeekEnabled(cls, date_to_test, day_mask):
    d = day_mask[date_to_test.weekday()]
    if (d != '-') and (d != '.'):
      return True
    return False