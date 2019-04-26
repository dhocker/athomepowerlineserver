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
# Timer storage
#

import timers.TimerProgram as TimerProgram
import database.Timers as Timers
import datetime
import threading
import logging

logger = logging.getLogger("server")

#######################################################################
# Singleton class for storing the set of timer programs (aka initiators)
#
# Note that to manipulate the timer program list, you must first
# acquire the list lock. When you are finished with the list you must
# release the list lock.
#
# The timer list is kept in memory because it is referenced frequently.
# Effectively, the in-memory list is a cache of the Timers table.
#
class TimerStore:

  # List of all timer programs
  TimerProgramList = []
  # Lock over the program list. See Acquire/Release methods below.
  TimerProgramListLock = threading.Lock()

  #######################################################################
  # Constructor
  def __init__(self):
    pass

  #######################################################################
  # Recover all of the timer programs from the database. Typically, this
  # is done at server start up.
  @classmethod
  def LoadTimerProgramList(cls):
    # Lock the list
    cls.AcquireTimerProgramList()

    try:
      cls.ClearTimerProgramList()

      rset = Timers.Timers.GetAll()
      for r in rset:
        name = r["name"]
        device_id = r["id"]
        day_mask = r["daymask"]
        start_trigger_method = r["starttriggermethod"]
        # We really want the on/off times to be in datetime format, not string format
        start_time = datetime.datetime.strptime(r["starttime"], "%Y-%m-%d %H:%M:%S")
        start_offset = int(r["startoffset"])
        start_randomize = True if r["startrandomize"] else False
        start_randomize_amount = r["startrandomizeamount"]
        stop_trigger_method = r["stoptriggermethod"]
        stop_time = datetime.datetime.strptime(r["stoptime"], "%Y-%m-%d %H:%M:%S")
        stop_offset = int(r["stopoffset"])
        stop_randomize = True if r["stoprandomize"] else False
        stop_randomize_amount = r["stoprandomizeamount"]
        start_action = r["startaction"]
        stop_action = r["stopaction"]
        security = r["security"]
        # Note that we don't do anything with the lastupdate column

        # Some debugging/tracing output
        logger.info("%s %d %s Start: {%s %s %s %s %s %s} Stop: {%s %s %s %s %s %s}",
                    name, device_id, day_mask,
                    start_trigger_method, start_time, start_offset, start_randomize, start_randomize_amount, start_action,
                    stop_trigger_method, stop_time, stop_offset, stop_randomize, stop_randomize_amount, stop_action)

        # Add each timer program to the current list of programs
        cls.AppendTimer(name, device_id, day_mask,
                        start_trigger_method, start_time, start_offset, start_randomize, start_randomize_amount,
                        stop_trigger_method, stop_time, stop_offset, stop_randomize, stop_randomize_amount,
                        start_action, stop_action, security)

      rset.close()
    finally:
      # Unlock the list
      cls.ReleaseTimerProgramList()

  #######################################################################
  # Save all of the timer programs to the database
  @classmethod
  def SaveTimerProgramList(cls):
    cls.AcquireTimerProgramList()

    try:
      # Clear the existing timer programs
      Timers.Timers.DeleteAll()

      logger.info("Saving all timer programs to database")
      for tp in cls.TimerProgramList:
        # print tp.name, tp.device_type, tp.device_address, tp.DayMask, tp.StartTime, tp.StopTime, tp.Security
        # print "Saving timer program:", tp.name
        # It may be necessary to format on/off time to be certain that the format is held across save/load
        # TODO Replace house-device-code with device id
        Timers.Timers.Insert(tp.Name, tp.device_id, tp.DayMask,
          tp.StartTriggerMethod, tp.StartTime, tp.StartOffset, tp.StartRandomize, tp.StartRandomizeAmount,
          tp.StopTriggerMethod, tp.StopTime, tp.StopOffset, tp.StopRandomize, tp.StopRandomizeAmount,
          tp.StartAction, tp.StopAction, tp.Security )
    finally:
      cls.ReleaseTimerProgramList()

  #######################################################################
  # Append a timer program to the end of the current list
  @classmethod
  def AppendTimer(cls, name, device_id, day_mask,
                  start_trigger_method, start_time, start_offset, start_randomize, start_randomize_amount,
                  stop_trigger_method, stop_time, stop_offset, stop_randomize, stop_randomize_amount,
                  start_action, stop_action, security = False):
    tp = TimerProgram.TimerProgram(name, int(device_id), day_mask,
      start_trigger_method, start_time, start_offset, start_randomize, start_randomize_amount,
      stop_trigger_method, stop_time, stop_offset, stop_randomize, stop_randomize_amount,
      start_action, stop_action, security)
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
    cls.TimerProgramListLock.acquire(True)
    return cls.TimerProgramList

  @classmethod
  def ReleaseTimerProgramList(cls):
    cls.TimerProgramListLock.release()

  #######################################################################
  # Debugging aid
  @classmethod
  def DumpTimerProgramList(cls):
    logger.info("Timer Program List Dump")
    for tp in cls.TimerProgramList:
      logger.info("%s %d %s %s %s %s %s %s %s %s %s %s %s %s %s %s", tp.Name, tp.device_id, tp.DayMask,
                  tp.StartTriggerMethod, tp.StartTime, tp.StartOffset, tp.StartRandomize, tp.StartRandomizeAmount,
                  tp.StopTriggerMethod, tp.StopTime, tp.StopOffset, tp.StopRandomize, tp.StopRandomizeAmount,
                  tp.StartAction, tp.StopAction, tp.Security)