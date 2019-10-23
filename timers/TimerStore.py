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
                id = r["id"]
                name = r["name"]
                device_id = r["deviceid"]
                day_mask = r["daymask"]
                trigger_method = r["triggermethod"]
                # We really want the on/off times to be in datetime format, not string format
                program_time = datetime.datetime.strptime(r["time"], "%Y-%m-%d %H:%M:%S")
                offset = int(r["offset"])
                randomize = True if r["randomize"] else False
                randomize_amount = r["randomizeamount"]
                action = r["command"]
                dimamount = r["dimamount"]
                # Note that we don't do anything with the lastupdate column

                # Some debugging/tracing output
                logger.info("%s %d %s Program: {%s %s %s %s %s %s %d}",
                            name, device_id, day_mask,
                            trigger_method, program_time, offset, randomize, randomize_amount,
                            action, dimamount)

                # Add each timer program to the current list of programs
                cls.AppendTimer(id, name, device_id, day_mask,
                                trigger_method, program_time, offset, randomize, randomize_amount,
                                action, dimamount)

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
                # Replace house-device-code with device id
                Timers.Timers.insert(tp.Name, tp.device_id, tp.DayMask,
                                     tp.TriggerMethod, tp.Time, tp.Offset, tp.Randomize,
                                     tp.RandomizeAmount,
                                     tp.Action, tp.Dimamount, tp.Security)
        finally:
            cls.ReleaseTimerProgramList()

    #######################################################################
    # Append a timer program to the end of the current list
    @classmethod
    def AppendTimer(cls, id, name, device_id, day_mask,
                    trigger_method, program_time, offset, randomize, randomize_amount,
                    action, dimamount, security=False):
        tp = TimerProgram.TimerProgram(id, name, int(device_id), day_mask,
                                       trigger_method, program_time, offset, randomize,
                                       randomize_amount,
                                       action, dimamount, security)
        cls.TimerProgramList.append(tp)

    @classmethod
    def UpdateTimer(cls, id, name, device_id, day_mask,
                    trigger_method, program_time, offset, randomize, randomize_amount,
                    action, dimamount, security=False):
        """
        Update an existing timer program entry
        :param id:
        :param name:
        :param device_id:
        :param day_mask:
        :param trigger_method:
        :param program_time:
        :param offset:
        :param randomize:
        :param randomize_amount:
        :param action:
        :param dimamount:
        :param security:
        :return:
        """
        timer_list = cls.AcquireTimerProgramList()

        try:
            # Remove the existing program
            try:
                for t in timer_list:
                    if t.id == id:
                        timer_list.remove(t)
                        break
            except:
                pass

            # Add the updated program as a new program
            tp = TimerProgram.TimerProgram(id, name, int(device_id), day_mask,
                                           trigger_method, program_time, offset, randomize,
                                           randomize_amount,
                                           action, dimamount, security)
            cls.TimerProgramList.append(tp)
        finally:
            cls.ReleaseTimerProgramList()

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
        try:
            for tp in cls.TimerProgramList:
                logger.debug("%d %s %d %s %s %s %d %d %d %s %d %d", tp.id, tp.Name, tp.device_id, tp.DayMask,
                            tp.TriggerMethod, tp.Time, tp.Offset, tp.Randomize, tp.RandomizeAmount,
                            tp.Action, tp.Dimamount, tp.Security)
        except Exception as ex:
            pass

