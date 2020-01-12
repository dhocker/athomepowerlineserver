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
# Programs table model
#

import database.AtHomePowerlineServerDb as AtHomePowerlineServerDb
from .base_table import BaseTable
import datetime


#######################################################################
class Programs(BaseTable):

    #######################################################################
    def __init__(self):
        pass

    #######################################################################
    # Empty all records from the Programs table
    @classmethod
    def DeleteAll(cls):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Programs")
        conn.commit()
        conn.close()
        return True

    # Return the set of all records in the Programs table
    # TODO Is this still used?
    @classmethod
    def GetAll(cls):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute(
            "SELECT * from Programs")
        return cls.rows_to_dict_list(rset)

    @classmethod
    def get_all_active_programs(cls):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute(
            'SELECT * FROM Programs WHERE command<>"none"')
        return cls.rows_to_dict_list(rset)

    @classmethod
    def get_all_device_programs(cls, device_id):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute(
            'SELECT Programs.* FROM ProgramAssignments JOIN Programs '
            'WHERE Programs.id=ProgramAssignments.program_id AND ProgramAssignments.device_id=:device_id',
            {"device_id": device_id})
        return cls.rows_to_dict_list(rset)

    @classmethod
    def get_program_by_id(cls, programid):
        """
        Return a specific Programs record
        :param programid:
        :return:
        """
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute(
            "SELECT * FROM Programs WHERE id=:programid", {"programid": programid})
        return cls.row_to_dict(rset.fetchone())

    #######################################################################
    # Insert a record into the Programs table.
    # This is not exactly optimized, but we don't expect to be saving that many programs.
    @classmethod
    def insert(cls, name, day_mask,
               trigger_method, program_time, offset, randomize, randomize_amount,
               action, dimamount, security):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        # SQL insertion safe...
        # Note that the current time is inserted as the update time. This is added to the
        # row as a convenient way to know when the program was stored. It isn't used for
        # any other purpose.
        c.execute("INSERT INTO Programs (name,daymask,triggermethod,time,offset,randomize,randomizeamount,command,dimamount,args,updatetime) " \
                  "values (?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)",
                  (name, day_mask,
                   trigger_method, program_time, offset, randomize, randomize_amount,
                   action, security, dimamount, datetime.datetime.now()))
        conn.commit()

        # Get id of inserted record
        id = c.lastrowid

        conn.close()
        return id

    @classmethod
    def update(cls, id, name, day_mask,
               trigger_method, program_time, offset, randomize, randomize_amount,
               action, dimamount, security):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("UPDATE Programs SET name=?,daymask=?,triggermethod=?,time=?,offset=?,randomize=?,randomizeamount=?,command=?,dimamount=?,args=?,updatetime=? " \
                  "WHERE id=?",
                  (name, day_mask,
                   trigger_method, program_time, offset, randomize, randomize_amount,
                   action, security, dimamount, datetime.datetime.now(), id))
        conn.commit()
        change_count = conn.total_changes
        conn.close()
        return change_count

    @classmethod
    def delete(cls, id):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Programs WHERE id=:id", {"id": id})
        conn.commit()
        change_count = conn.total_changes
        conn.close()
        return change_count
