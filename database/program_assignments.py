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

    @classmethod
    def insert(cls, device_id, program_id):
        """
        Insert a program assignment record
        :param device_id: The target device ID
        :param program_id: The program to be assigned
        :return:
        """
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)

        c.execute("INSERT INTO ProgramAssignments (device_id,program_id) values (?,?)",
                  (device_id, program_id))
        id = c.lastrowid
        conn.commit()
        conn.close()
        return id
