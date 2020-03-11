# -*- coding: utf-8 -*-
#
# AtHomePowerlineServer
# Copyright © 2014, 2020  Dave Hocker
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

from database.AtHomePowerlineServerDb import AtHomePowerlineServerDb
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
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Programs")
        conn.commit()
        conn.close()
        return True

    def get_all_programs(self):
        """
        Return the set of all records in the Programs table
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                "SELECT * from Programs"
            )
            result = Programs.rows_to_dict_list(rset)
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            result = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return result

    def get_all_active_programs(self):
        """
        Return the set of all records where the program command is not none
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                'SELECT * FROM Programs WHERE command<>"none"'
            )
            result = Programs.rows_to_dict_list(rset)
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            result = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return result

    def get_all_device_programs(self, device_id):
        """
        Return the set of programs for a given device
        :param device_id:
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                'SELECT Programs.* FROM ProgramAssignments JOIN Programs '
                'WHERE Programs.id=ProgramAssignments.program_id AND ProgramAssignments.device_id=:device_id',
                {"device_id": device_id}
            )
            result = Programs.rows_to_dict_list(rset)
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            result = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return result

    def get_all_available_programs(self, device_id):
        """
        Return all programs that ARE NOT assigned to a device
        :param device_id:
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                'SELECT * FROM Programs '
                'WHERE Programs.id NOT IN (SELECT program_id from ProgramAssignments where device_id=:device_id) '
                'ORDER BY name',
                {"device_id": device_id}
            )
            result = Programs.rows_to_dict_list(rset)
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            result = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return result

    def get_program_by_id(self, programid):
        """
        Return a specific Programs record
        :param programid:
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                "SELECT * FROM Programs WHERE id=:programid",
                {"programid": programid}
            )
            result = Programs.row_to_dict(rset.fetchone())
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            result = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return result

    def insert(self, name, day_mask,
               trigger_method, program_time, offset, randomize, randomize_amount,
               action, color, brightness):
        """
        Insert a record into the Programs table.
        :param name:
        :param day_mask:
        :param trigger_method:
        :param program_time:
        :param offset:
        :param randomize:
        :param randomize_amount:
        :param action:
        :param color:
        :param brightness:
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            c.execute(
                "INSERT INTO Programs (name,daymask,triggermethod,time,offset,randomize,randomizeamount,command,color,brightness,updatetime) " \
                "values (?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)",
                (name, day_mask,
                 trigger_method, program_time, offset, randomize, randomize_amount,
                 action, color, brightness, datetime.datetime.now())
            )
            conn.commit()

            # Get id of inserted record
            id = c.lastrowid
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            id = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return id

    def update(self, id, name, day_mask,
               trigger_method, program_time, offset, randomize, randomize_amount,
               action, color, brightness):
        """
        Update a program record
        :param id:
        :param name:
        :param day_mask:
        :param trigger_method:
        :param program_time:
        :param offset:
        :param randomize:
        :param randomize_amount:
        :param action:
        :param color:
        :param brightness:
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            c.execute(
                "UPDATE Programs SET name=?,daymask=?,triggermethod=?,time=?,offset=?,randomize=?,randomizeamount=?,command=?,color=?,brightness=?,updatetime=? " \
                "WHERE id=?",
                (name, day_mask,
                 trigger_method, program_time, offset, randomize, randomize_amount,
                 action, color, brightness, datetime.datetime.now(), id)
            )
            conn.commit()
            change_count = conn.total_changes
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            change_count = 0
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return change_count

    def delete(self, id):
        """
        Delete a given program record
        :param id:
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            c.execute(
                "DELETE FROM Programs WHERE id=:id", {"id": id}
            )
            conn.commit()
            change_count = conn.total_changes
        except Exception as ex:
            self.set_last_error(Programs.SERVER_ERROR, str(ex))
            change_count = 0
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return change_count
