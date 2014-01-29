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
# Timer program - represents the equivalent of a timer initiator
#
# The program is limited to turning a device on then off
#

#######################################################################
class TimerProgram:

  #######################################################################
  # Instance constructor
  def __init__(self, name, house_device_code, day_mask, on_time, off_time, security):
    self.name = name
    self.HouseDeviceCode = house_device_code
    self.DayMask = day_mask
    self.OnTime = on_time
    self.OffTime = off_time
    self.Security = security

    # These are used to monitor the timer events
    self.OnEventRun = False
    self.OffEventRun = False
  
  # Decode day mask format into an array where [0] is Monday
  # and [6] is Sunday.
  # Day mask format: MTWTFSS (Monday through Sunday)
  # Event days have the letter while non-event days have a '-'
  def DecodeDayMask(self, day_mask):
    # Sunday through to Saturday
    effective_days = [False, False, False, False, False, False, False]

    for dx in range(0, 7):
      if (day_mask[dx] != '-') and (day_mask[dx] != '.'):
        effective_days[dx] = True
    
    return effective_days
    