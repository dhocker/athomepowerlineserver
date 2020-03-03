#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright © 2014, 2020  Dave Hocker
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
import random
from helpers.TimeZone import TimeZone
from helpers.sun_data import get_sunrise, get_sunset
from database.managed_devices import ManagedDevices
from database.programs import Programs
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
            logger.info("Program timer checks sleeping...")
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
                logger.info("Program timer checks starting...")
                self.RunTimerPrograms()
                logger.info("Program timer checks ended")

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
        # All of the Programs records where command is not "none"
        tp_list = Programs.get_all_active_programs()

        for tp in tp_list:
            try:
                self.RunTimerProgram(tp)
            except Exception as ex:
                logger.error("Unhandled exception caught while running timer program %s id=%d", tp["name"], tp["id"])
                logger.error(ex)
                logger.debug(traceback.format_exc())
            finally:
                pass

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
        if TimerServiceThread.IsDayOfWeekEnabled(now, tp["daymask"]):
            # we consider the event triggered if the current date/time in hours and minutes matches the event time
            logger.debug(str(tp))

            # Event check
            if self.IsEventTriggered(tp):
                # Event triggered
                logger.info("Program event triggered: %s %s", tp["name"], tp["command"])
                # Fire the action
                self.RunTimerAction(tp)
        else:
            logger.debug("%s is not enabled for the current weekday", tp["name"])

    ########################################################################
    # Run an action
    def RunTimerAction(self, tp):
        # Get all devices that have been assigned this program
        devices = ManagedDevices.get_devices_for_program(tp["id"])
        for device_rec in devices:
            device_mfg = device_rec["mfg"]
            device_name = device_rec["name"]
            device_address = device_rec["address"]
            device_channel = device_rec["channel"]
            # color and brightness from the program
            device_color = tp["color"]
            device_brightness = tp["brightness"]
            logger.info("Executing action: %s %s %s %s", tp["command"], device_mfg, device_address, device_channel)
            ActionFactory.RunAction(tp["command"], device_rec["id"], device_mfg, device_name, device_address,
                                    device_channel, device_color, device_brightness)

    ########################################################################
    # Test a date to see if its weekday is enabled
    @classmethod
    def IsDayOfWeekEnabled(cls, date_to_test, day_mask):
        d = day_mask[date_to_test.weekday()]
        if (d != '-') and (d != '.'):
            return True
        return False

    @classmethod
    def IsEventTriggered(cls, tp):
        """
        Test the program against the given time to see if the start event has occurred.
        :param tp: Timer program record
        :return:
        """
        # We use the time part of the datetime to mean the time TODAY.
        now = datetime.datetime.now()

        # time without seconds
        now_dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0, tzinfo=TimeZone())

        # Randomized amount
        randomized_amount = 0
        if tp["randomize"]:
            randomized_amount = cls.GetRandomizedAmount(tp["randomizeamount"])
        logger.debug("Randomize amount: %s", randomized_amount)

        # Factory testing based on trigger method
        pt = datetime.datetime.strptime(tp["time"], "%Y-%m-%d %H:%M:%S")
        if tp["triggermethod"] == "clock-time":
            today_time = datetime.datetime(now.year, now.month, now.day, pt.hour,
                                                pt.minute, pt.second, tzinfo=TimeZone())
            today_time = today_time + datetime.timedelta(minutes=(tp["offset"] + randomized_amount))
            return today_time == now_dt
        elif tp["triggermethod"] == "sunset":
            # logger.debug("Testing sunset trigger")
            sunset = get_sunset(now_dt)
            offset_sunset = sunset + datetime.timedelta(minutes=(tp["offset"] + randomized_amount))
            return now_dt == offset_sunset
        elif tp["triggermethod"] == "sunrise":
            # logger.debug("Testing sunrise trigger")
            sunrise = get_sunrise(now_dt)
            offset_sunrise = sunrise + datetime.timedelta(minutes=(tp["offset"] + randomized_amount))
            return now_dt == offset_sunrise

        # "none" falls to here
        return False


    @classmethod
    def GetRandomizedAmount(cls, randomize_amount):
        """
        For today's date, calculate the integer randomized amount r where
        -randomize_amount <= int(r) <= randomize_amount
        """

        # Today's randomization factor
        rf = cls.GetRandomFactor()

        # Round randomized value to a whole integer
        # Return the result as an integer
        return int(round(rf * float(randomize_amount)))

    @classmethod
    def GetRandomFactor(cls):
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
