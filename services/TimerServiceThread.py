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
# TimerService thread
#

import threading
import time
import datetime
import logging
import traceback
import timers.TimerStore
import timers.TimerProgram
from database.devices import Devices
import commands.ActionFactory as ActionFactory

logger = logging.getLogger("server")


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
        self.terminate_signal = threading.Event()

    ########################################################################
    # Called by threading on the new thread
    def run(self):
        # logger.info("Timer service running")

        # Check the terminate signal every second
        while not self.terminate_signal.isSet():
            logger.info("Timer checks sleep")
            # This sleeps until the next minute.
            # We sleep in a granular fashion so that
            # a service stop/restart command takes effect
            # in a minimal amount of time.
            wait_time = 60 - datetime.datetime.now().second
            while (wait_time > 0) and (not self.terminate_signal.isSet()):
                time.sleep(1)
                wait_time -= 1

            # Every minute run the program checks if terminate is not set
            if not self.terminate_signal.isSet():
                logger.info("Timer checks start")
                self.RunTimerPrograms()
                logger.info("Timer checks end")

    ########################################################################
    # Terminate the timer service thread
    def Terminate(self):
        self.terminate_signal.set()
        # wait for service thread to exit - could be a while
        logger.info("Waiting for timer service to stop...this could take a few seconds")
        self.join()
        logger.info("Timer service stopped")

    ########################################################################
    # Run timer programs that have reached their trigger time
    def RunTimerPrograms(self):
        tp_list = timers.TimerStore.TimerStore.AcquireTimerProgramList()
        logger.info("RunTimerPrograms lock acquired")

        try:
            for tp in tp_list:
                self.RunTimerProgram(tp)
        except Exception as ex:
            logger.error("Exception caught while running timer programs")
            logger.error(ex)
            logger.debug(traceback.format_exc())
        finally:
            timers.TimerStore.TimerStore.ReleaseTimerProgramList()
            logger.info("RunTimerPrograms lock released")

    ########################################################################
    # Run a single timer program
    def RunTimerProgram(self, tp):
        # The date in a timer program's on/off time has no meaning.
        # We use the time part of the datetime to mean the time TODAY.
        now = datetime.datetime.now()

        # TODO Answer question about persisting event status in database (and resetting status at well defined times)
        # This will only be interesting if we want to manage events that may have occurred BEFORE
        # the server was started. That will be a complicated task.

        # Only if the current day is enabled...
        if TimerServiceThread.IsDayOfWeekEnabled(now, tp.DayMask):
            # we consider the event triggered if the current date/time in hours and minutes matches the event time
            logger.debug(str(tp))

            # Event check
            if tp.IsEventTriggered():
                # Event triggered
                tp.EventRun = True
                logger.info("TimerProgram event triggered: %s %s", tp.Name, tp.Action)
                # Fire the action
                self.RunTimerAction(tp)
        else:
            logger.debug("%s is not enabled for the current weekday", tp.Name)

    ########################################################################
    # Run an action
    def RunTimerAction(self, tp):
        device_rec = Devices.get_device_by_id(tp.device_id)
        device_type = device_rec["type"]
        device_name = device_rec["name"]
        device_address = device_rec["address"]
        logger.info("Executing action: %s %s %s", tp.Action, device_type, device_address)
        ActionFactory.RunAction(tp.Action, tp.device_id, device_type, device_name, device_address, int(tp.Dimamount))

    ########################################################################
    # Test a date to see if its weekday is enabled
    @classmethod
    def IsDayOfWeekEnabled(cls, date_to_test, day_mask):
        d = day_mask[date_to_test.weekday()]
        if (d != '-') and (d != '.'):
            return True
        return False
