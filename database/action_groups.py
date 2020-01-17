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


class ActionGroups(BaseTable):
    def __init__(self):
        pass

    @classmethod
    def get_all_groups(cls):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        # The results are sorted based on the most probable use
        rset = c.execute("SELECT * from ActionGroups ORDER BY name")
        return cls.rows_to_dict_list(rset)

    @classmethod
    def get_group_devices(cls, id):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        # The results are sorted based on the most probable use
        rset = c.execute("SELECT * from ActionGroups WHERE id=:id", {"id": id})
        return cls.row_to_dict(rset.fetchone())

    @classmethod
    def get_group_by_id(cls, id):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        # The results are sorted based on the most probable use
        rset = c.execute("SELECT * from ActionGroups WHERE id=:id", {"id": id})
        return cls.row_to_dict(rset.fetchone())

    @classmethod
    def insert(cls, group_name):
        """
        Insert a group record
        :param name: The name of the new group
        :return:
        """
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)

        c.execute("INSERT INTO ActionGroups (name) values (:group_name)", {"group_name": group_name})
        id = c.lastrowid
        conn.commit()
        conn.close()
        return id

    @classmethod
    def update(cls, id, name):
        """
        Update a group record
        :param name: The name of the group
        :return:
        """
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)

        c.execute("UPDATE ActionGroups SET name=? WHERE id=?",
                  (name, id))
        conn.commit()
        change_count = conn.total_changes
        conn.close()
        return change_count

    @classmethod
    def delete(cls, id):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM ActionGroups WHERE id=:id",
                  {"id": id})
        conn.commit()
        change_count = conn.total_changes
        conn.close()
        return change_count
