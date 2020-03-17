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

    def get_group_devices(self, group_id):
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                "SELECT * from ManagedDevices "
                "JOIN ActionGroupDevices ON ActionGroupDevices.group_id=:group_id "
                "WHERE ManagedDevices.id=ActionGroupDevices.device_id", {"group_id": group_id}
            )
            result = ActionGroupDevices.rows_to_dict_list(rset)
        except Exception as ex:
            self.set_last_error(ActionGroupDevices.SERVER_ERROR, str(ex))
            result = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return result

    def insert_device(self, group_id, device_id):
        """
        Insert a group device record
        :param group_id: The containing group ID
        :param device_id: The devid ID being added to the group
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            c.execute(
                "INSERT INTO ActionGroupDevices (group_id,device_id) values (?,?)",
                (group_id, device_id)
            )
            conn.commit()

            # Get id of inserted record
            id = c.lastrowid
        except Exception as ex:
            self.set_last_error(ActionGroupDevices.SERVER_ERROR, str(ex))
            id = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return id

    def delete_device(self, group_id, device_id):
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            c.execute(
                "DELETE FROM ActionGroupDevices WHERE group_id=:group_id AND device_id=:device_id",
                {"group_id": group_id, "device_id": device_id}
            )
            conn.commit()
            change_count = conn.total_changes
        except Exception as ex:
            self.set_last_error(ActionGroupDevices.SERVER_ERROR, str(ex))
            change_count = 0
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return change_count
