# -*- coding: utf-8 -*-
#
# AtHomePowerlineServer
# Copyright © 2020  Dave Hocker
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


class ProgramAssignments(BaseTable):
    def __init__(self):
        pass

    def insert(self, device_id, program_id):
        """
        Insert a program assignment record
        :param device_id: The target device ID
        :param program_id: The program to be assigned
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            c.execute(
                "INSERT INTO ProgramAssignments (device_id,program_id) values (?,?)",
                (device_id, program_id)
            )
            conn.commit()

            # Get id of inserted record
            id = c.lastrowid
        except Exception as ex:
            self.set_last_error(ProgramAssignments.SERVER_ERROR, str(ex))
            id = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return id

    def delete(self, device_id, program_id):
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            c.execute(
                "DELETE FROM ProgramAssignments WHERE device_id=:device_id AND program_id=:program_id",
                {"device_id": device_id, "program_id": program_id}
            )
            conn.commit()
            change_count = conn.total_changes
        except Exception as ex:
            self.set_last_error(ProgramAssignments.SERVER_ERROR, str(ex))
            change_count = 0
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return change_count

    def is_assigned(self, device_id, program_id):
        """
        Answers the question: Is this program assigned to the given device?
        :param device_id:
        :param program_id:
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                'SELECT * FROM ProgramAssignments '
                'WHERE ProgramAssignments.device_id=:device_id AND ProgramAssignments.program_id=:program_id',
                {"device_id": device_id, "program_id": program_id}
            )
            program_is_assigned = rset.fetchone() is not None
            conn.close()
        except Exception as ex:
            self.set_last_error(ProgramAssignments.SERVER_ERROR, str(ex))
            program_is_assigned = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return program_is_assigned
