#
# Timer storage
#

import TimerProgram
import database.Timers
import datetime

#######################################################################
# Singleton class for storing the set of timer programs (aka initiators)
class TimerStore:

  # List of all timer programs
  TimerProgramList = []

  #######################################################################
  # Constructor
  def __init__(self):
    pass

  #######################################################################
  # Recover all of the timer programs from the database. Typcially, this
  # is done at server start up.
  @classmethod
  def LoadTimerProgramList(cls):
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

  #######################################################################
  # Save all of the timer programs to the database
  @classmethod
  def SaveTimerProgramList(cls):
    # Clear the existing timer programs
    database.Timers.Timers.DeleteAll()

    print "Saving all timer programs to database"
    for tp in cls.TimerProgramList:
      # print tp.name, tp.HouseDeviceCode, tp.DayMask, tp.OnTime, tp.OffTime, tp.Security    
      # print "Saving timer program:", tp.name
      # It may be necessary to format on/off time to be certain that the format is held across save/load
      database.Timers.Timers.Insert(tp.name, tp.HouseDeviceCode, tp.DayMask, tp.OnTime, tp.OffTime, tp.Security )

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
  # Debugging aid
  @classmethod
  def DumpTimerProgramList(cls):
    print "Timer Program List Dump"
    for tp in cls.TimerProgramList:
      print tp.name, tp.HouseDeviceCode, tp.DayMask, tp.OnTime, tp.OffTime, tp.Security