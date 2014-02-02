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

#
# TimerService thread
#

import threading
import time
import datetime
import timers.TimerStore
import timers.TimerProgram

# The timer service thread periodically examines the list of timer programs.
# When a timer event expires, it transmits the appropriate X10 function.
class TimerServiceThread(threading.Thread):

  # Constructor
  def __init__(self, thread_id, name):
    threading.Thread.__init__(self)
    self.thread_id = thread_id
    self.name = name
    self.terminate_signal = False

  # Called by threading on the new thread
  def run(self):
    # print "Timer service running"

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
        print datetime.datetime.now()
        self.RunTimerPrograms()

  # Terminate the timer service thread
  def Terminate(self):
    self.terminate_signal = True
    # wait for service thread to exit - could be a while
    print "Waiting for timer service to stop...this could take a few seconds"
    self.join()
    print "Timer service stopped"

  # Run timer programs that have reached their trigger time
  def RunTimerPrograms(self):
    tp_list = timers.TimerStore.TimerStore.AcquireTimerProgramList()

    try:
      for tp in tp_list:
        self.RunTimerProgram(tp)
    finally:
      timers.TimerStore.TimerStore.ReleaseTimerProgramList()
  
  # Run a single timer program
  def RunTimerProgram(self, tp):
    # The date in a timer program's on/off time has no meaning.
    # We use the time part of the datetime to mean the time TODAY.
    now = datetime.datetime.now()
    # On/Off times for TODAY
    today_starttime = datetime.datetime(now.year, now.month, now.day, tp.StartTime.hour, tp.StartTime.minute, tp.StartTime.second)
    today_stoptime = datetime.datetime(now.year, now.month, now.day, tp.StopTime.hour, tp.StopTime.minute, tp.StopTime.second)

    print tp.HouseDeviceCode, tp.DecodeDayMask(tp.DayMask)

    # TODO Develop algorithm for reasonable triggering of on/start and off/stop events

    # TODO Answer question about persisting event status in database (and resetting status at well defined times)

    # time without seconds
    now_dt = datetime.datetime(1900, 1, 1, now.hour, now.minute, 0)

    # we consider the event triggered if the current date/time in hours and minutes matches the event time
    print "Start:", tp.StartTime, now_dt
    print "Stop:", tp.StopTime, now_dt

    if (not tp.StartEventRun) and (tp.StartTime == now_dt):
      # Start event triggered
      tp.StartEventRun = True
      print "Start event triggered: ", tp.Name, tp.StartTime, tp.StartAction
      pass
    if (not tp.StopEventRun) and (tp.StopTime == now_dt):
      # Stop event triggered
      tp.StopEventRun = True
      print "Start event triggered: ", tp.Name, tp.StopTime, tp.StopAction
      pass
