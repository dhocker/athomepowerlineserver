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
    def __init__(self, id, name, device_id, day_mask,
                 trigger_method, program_time, offset, randomize, randomize_amount,
                 action, dimamount, security):
        self.id = id
        self.Name = name
        self.device_id = device_id
        self.DayMask = day_mask
        self.TriggerMethod = trigger_method
        self.Time = program_time
        self.Offset = offset
        self.Randomize = randomize
        self.RandomizeAmount = randomize_amount
        self.Action = action
        self.Dimamount = dimamount
        self.Security = security

        # These are used to monitor the timer events
        self.EventRun = False

    def __str__(self):
        """
        Custom str implementation
        """
        s = "id={0} {1} {2} {3} ".format(self.id, self.Name, self.device_id, self.DayMask)

        if self.TriggerMethod == "clock-time":
            s = s + "Trigger: {0} {1} ".format(self.TriggerMethod, self.Time)
        else:
            s = s + "Trigger: {0} {1} ".format(self.TriggerMethod, self.Offset)
        s = s + "Randomize: {0} {1} ".format(self.Randomize, self.RandomizeAmount)

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

    def IsEventTriggered(self):
        """
        Test the program against the given time to see if the start event has occurred.
        """

        # We use the time part of the datetime to mean the time TODAY.
        now = datetime.datetime.now()

        # time without seconds
        now_dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0, tzinfo=TimeZone())

        # Randomized amount
        randomized_amount = 0
        if self.Randomize:
            randomized_amount = self.GetRandomizedAmount(self.RandomizeAmount)
        logger.debug("Randomize amount: %s", randomized_amount)

        # Factory testing based on trigger method
        if self.TriggerMethod == "clock-time":
            today_time = datetime.datetime(now.year, now.month, now.day, self.Time.hour,
                                                self.Time.minute, self.Time.second, tzinfo=TimeZone())
            today_time = today_time + datetime.timedelta(minutes=(self.Offset + randomized_amount))
            return today_time == now_dt
        elif self.TriggerMethod == "sunset":
            # logger.debug("Testing sunset trigger")
            sunset = get_sunset(now_dt)
            offset_sunset = sunset + datetime.timedelta(minutes=(self.Offset + randomized_amount))
            return now_dt == offset_sunset
        elif self.TriggerMethod == "sunrise":
            # logger.debug("Testing sunrise trigger")
            sunrise = get_sunrise(now_dt)
            offset_sunrise = sunrise + datetime.timedelta(minutes=(self.Offset + randomized_amount))
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
