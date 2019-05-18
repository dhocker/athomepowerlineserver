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
from .base_table import BaseTable
import datetime


#######################################################################
class Timers(BaseTable):

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

    # Return the set of all records in the Timers table
    @classmethod
    def GetAll(cls):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute(
            "SELECT Timers.*, Devices.type, Devices.address from Timers join Devices on Timers.deviceid=Devices.id")
        return rset

    @classmethod
    def get_all_device_programs(cls, deviceid):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute(
            "SELECT * FROM Timers WHERE deviceid=:deviceid", {"deviceid": deviceid})
        return cls.rows_to_dict_list(rset)

    #######################################################################
    # Insert a record into the Timers table.
    # This is not exactly optimized, but we don't expect to be saving that many timer programs.
    @classmethod
    def insert(cls, name, device_id, day_mask,
               trigger_method, program_time, offset, randomize, randomize_amount,
               action, dimamount, security):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        # SQL insertion safe...
        # Note that the current time is inserted as the update time. This is added to the
        # row as a convenient way to know when the timer was stored. It isn't used for
        # any other purpose.
        c.execute("INSERT INTO Timers (name,deviceid,daymask,triggermethod,time,offset,randomize,randomizeamount,command,dimamount,args,updatetime) " \
                  "values (?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?)",
                  (name, device_id, day_mask,
                   trigger_method, program_time, offset, randomize, randomize_amount,
                   action, security, dimamount, datetime.datetime.now()))
        conn.commit()

        # Get id of inserted record
        id = c.lastrowid

        conn.close()
        return id

    @classmethod
    def update(cls, id, name, device_id, day_mask,
               trigger_method, program_time, offset, randomize, randomize_amount,
               action, dimamount, security):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("UPDATE Timers SET name=?,deviceid=?,daymask=?,triggermethod=?,time=?,offset=?,randomize=?,randomizeamount=?,command=?,dimamount=?,args=?,updatetime=? " \
                  "WHERE id=?",
                  (name, device_id, day_mask,
                   trigger_method, program_time, offset, randomize, randomize_amount,
                   action, security, dimamount, datetime.datetime.now(), id))
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, id):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Timers WHERE id=?", (id))
        conn.commit()
        conn.close()
