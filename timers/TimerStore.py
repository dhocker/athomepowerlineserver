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
# Timer storage
#

import TimerProgram
import database.Timers
import datetime
import threading

#######################################################################
# Singleton class for storing the set of timer programs (aka initiators)
class TimerStore:

  # List of all timer programs
  TimerProgramList = []
  # Lock over the program list
  TimerProgramListLock = threading.Lock()

  #######################################################################
  # Constructor
  def __init__(self):
    pass

  #######################################################################
  # Recover all of the timer programs from the database. Typcially, this
  # is done at server start up.
  @classmethod
  def LoadTimerProgramList(cls):
    # Lock the list
    cls.AcquireTimerProgramList()

    cls.ClearTimerProgramList()

    rset = database.Timers.Timers.GetAll()
    for r in rset:
      name = r["name"]
      house_device_code = r["housedevicecode"]
      day_mask = r["daymask"]
      # We really want the on/off times to be in datetime format, not string format
      on_time = datetime.datetime.strptime(r["ontime"], "%Y-%m-%d %H:%M:%S")
      off_time = datetime.datetime.strptime(r["offtime"], "%Y-%m-%d %H:%M:%S")
      security = r["security"]
      # Note that we don't do anything with the lastupdate column

      # Some debugging/tracing output
      print name #, type(on_time), on_time, type(off_time), off_time

      # Add each timer program to the current list of programs
      cls.AppendTimer(name, house_device_code, day_mask, on_time, off_time, security)

    rset.close()
    # Unlock the list
    cls.ReleaseTimerProgramList()

  #######################################################################
  # Save all of the timer programs to the database
  @classmethod
  def SaveTimerProgramList(cls):
    cls.AcquireTimerProgramList()

    # Clear the existing timer programs
    database.Timers.Timers.DeleteAll()

    print "Saving all timer programs to database"
    for tp in cls.TimerProgramList:
      # print tp.name, tp.HouseDeviceCode, tp.DayMask, tp.OnTime, tp.OffTime, tp.Security    
      # print "Saving timer program:", tp.name
      # It may be necessary to format on/off time to be certain that the format is held across save/load
      database.Timers.Timers.Insert(tp.name, tp.HouseDeviceCode, tp.DayMask, tp.OnTime, tp.OffTime, tp.Security )

    cls.ReleaseTimerProgramList()

  #######################################################################
  # Append a timer program to the end of the current list
  @classmethod
  def AppendTimer(cls, name, house_device_code, day_mask, on_time, off_time, security = False):
    tp = TimerProgram.TimerProgram(name, house_device_code, day_mask, on_time, off_time, security)
    cls.TimerProgramList.append(tp)

  #######################################################################
  # Reset the current program list
  @classmethod
  def ClearTimerProgramList(cls):
    cls.TimerProgramList = []

  #######################################################################
  # Return the timer program list in a locked state
  @classmethod
  def AcquireTimerProgramList(cls):
    # Wait for lock
    cls.TimerProgramListLock.acquire(1)
    return cls.TimerProgramList

  @classmethod
  def ReleaseTimerProgramList(cls):
    cls.TimerProgramListLock.release()

  #######################################################################
  # Debugging aid
  @classmethod
  def DumpTimerProgramList(cls):
    print "Timer Program List Dump"
    for tp in cls.TimerProgramList:
      print tp.name, tp.HouseDeviceCode, tp.DayMask, tp.OnTime, tp.OffTime, tp.Security