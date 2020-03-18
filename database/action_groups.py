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

    def get_all_groups(self):
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                "SELECT * from ActionGroups ORDER BY name"
            )
            result = ActionGroups.rows_to_dict_list(rset)
        except Exception as ex:
            self.last_error_code = ActionGroups.SERVER_ERROR
            self.last_error = str(ex)
            result = None
        finally:
            # Make sure connection is closed
            if conn:
                conn.close()

        return result

    # def get_group_devices(self, id):
    #     self.clear_last_error()
    #
    #     conn = None
    #     try:
    #         conn = AtHomePowerlineServerDb.GetConnection()
    #         c = AtHomePowerlineServerDb.GetCursor(conn)
    #         # The results are sorted based on the most probable use
    #         rset = c.execute(
    #             "SELECT * from ActionGroups WHERE id=:id", {"id": id}
    #         )
    #         result = ActionGroups.row_to_dict(rset.fetchone())
    #     except Exception as ex:
    #         self.set_last_error(ActionGroups.SERVER_ERROR, str(ex))
    #         result = None
    #     finally:
    #         # Make sure connection is closed
    #         if conn is not None:
    #             conn.close()
    #
    #     return result

    def get_group_by_id(self, id):
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            # The results are sorted based on the most probable use
            rset = c.execute(
                "SELECT * from ActionGroups WHERE id=:id", {"id": id}
            )
            result = ActionGroups.row_to_dict(rset.fetchone())
        except Exception as ex:
            self.set_last_error(ActionGroups.SERVER_ERROR, str(ex))
            result = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return result

    def insert(self, group_name):
        """
        Insert a group record
        :param group_name: The name of the new group
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            c.execute(
                "INSERT INTO ActionGroups (name) values (:group_name)", {"group_name": group_name}
            )
            conn.commit()

            # Get id of inserted record
            id = c.lastrowid
        except Exception as ex:
            self.set_last_error(ActionGroups.SERVER_ERROR, str(ex))
            id = None
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return id

    def update(self, id, name):
        """
        Update a group record
        :param id:
        :param name: The name of the group
        :return:
        """
        self.clear_last_error()

        conn = None
        try:
            conn = AtHomePowerlineServerDb.GetConnection()
            c = AtHomePowerlineServerDb.GetCursor(conn)
            c.execute(
                "UPDATE ActionGroups SET name=? WHERE id=?",
                (name, id)
            )
            conn.commit()
            change_count = conn.total_changes
        except Exception as ex:
            self.set_last_error(ActionGroups.SERVER_ERROR, str(ex))
            change_count = 0
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return change_count

    def delete(self, id):
        """
        Delete a record by its ID
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
                "DELETE FROM ActionGroups WHERE id=:id",
                {"id": id}
            )
            conn.commit()
            change_count = conn.total_changes
        except Exception as ex:
            self.set_last_error(ActionGroups.SERVER_ERROR, str(ex))
            change_count = 0
        finally:
            # Make sure connection is closed
            if conn is not None:
                conn.close()

        return change_count
