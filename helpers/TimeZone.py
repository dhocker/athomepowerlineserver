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

import datetime
import time


class TimeZone(datetime.tzinfo):
    '''
    Used with datetime objects to get a complete ISO timestamp.
    Reference: http://agiliq.com/blog/2009/02/understanding-datetime-tzinfo-timedelta-amp-timezo/
    '''
    def utcoffset(self, dt):
        # Note that timezone is in seconds and it is a positive number for the US.
        # We make it negative for ISO format
        timezone = time.timezone
        offset = (-timezone) / 3600
        if time.localtime().tm_isdst:
            offset += 1
        return datetime.timedelta(hours=offset)
