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


class ActionGroupDevices(BaseTable):
    def __init__(self):
        pass

    @classmethod
    def get_group_devices(cls, group_id):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        # The results are sorted based on the most probable use
        rset = c.execute("SELECT * from ManagedDevices "
                         "JOIN ActionGroupDevices ON ActionGroupDevices.group_id=:group_id "
                         "WHERE ManagedDevices.id=ActionGroupDevices.device_id", {"group_id": group_id})
        return cls.rows_to_dict_list(rset)

    @classmethod
    def insert_device(cls, group_id, device_id):
        """
        Insert a group device record
        :param group_id: The containing group ID
        :param device_id: The devid ID being added to the group
        :return:
        """
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)

        c.execute("INSERT INTO ActionGroupDevices (group_id,device_id) values (?,?)",
                  (group_id, device_id))
        id = c.lastrowid
        conn.commit()
        conn.close()
        return id

    @classmethod
    def delete_device(cls, group_id, device_id):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM ActionGroupDevices WHERE group_id=:group_id AND device_id=:device_id",
                  {"group_id": group_id, "device_id": device_id})
        conn.commit()
        change_count = conn.total_changes
        conn.close()
        return change_count
