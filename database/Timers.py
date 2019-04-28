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
# Timers table model
#

import database.AtHomePowerlineServerDb as AtHomePowerlineServerDb
import datetime


#######################################################################
class Timers:

    #######################################################################
    def __init__(self):
        pass

    #######################################################################
    # Empty all records from the Timers table
    @classmethod
    def DeleteAll(cls):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Timers")
        conn.commit()
        conn.close()

        #######################################################################

    # Return the set of all records in the Timers table
    @classmethod
    def GetAll(cls):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute(
            "SELECT Timers.*, Devices.id, Devices.type, Devices.address from Timers join Devices on Timers.deviceid=Devices.id")
        return rset

    #######################################################################
    # Insert a record into the Timers table.
    # This is not exactly optimized, but we don't expect to be saving that many timer programs.
    @classmethod
    def Insert(cls, name, device_id, day_mask,
               start_trigger_method, start_time, start_offset, start_randomize, start_randomize_amount,
               stop_trigger_method, stop_time, stop_offset, stop_randomize, stop_randomize_amount,
               start_action, stop_action, security):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        # SQL insertion safe...
        # Note that the current time is inserted as the update time. This is added to the
        # row as a convenient way to know when the timer was stored. It isn't used for
        # any other purpose.
        c.execute("INSERT INTO Timers values (?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, device_id, day_mask,
                   start_trigger_method, start_time, start_offset, start_randomize, start_randomize_amount,
                   stop_trigger_method, stop_time, stop_offset, stop_randomize, stop_randomize_amount,
                   start_action, stop_action, security, datetime.datetime.now()))
        conn.commit()
        conn.close()
