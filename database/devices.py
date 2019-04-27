#
# Timers table model
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from database.AtHomePowerlineServerDb import AtHomePowerlineServerDb
import datetime
import logging

logger = logging.getLogger("server")


class Devices:

    #######################################################################
    def __init__(self):
        pass

    #######################################################################
    # Empty all records from the Devices table
    @classmethod
    def delete_all(cls):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Devices")
        conn.commit()
        conn.close()

    @classmethod
    def get_device_by_id(cls, device_id):
        """
        Return the dvice record for a given device
        :param device_id: The device id (key)
        :return: device record as a dict
        """
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute("SELECT * from Devices where id=?", str(device_id))
        return cls.row_to_dict(rset.fetchone())

    @classmethod
    def row_to_dict(cls, row):
        """
        Convert an SQLite row set to a dict
        :param row: the row set to be converted
        :return: a dict containing all of the columns in the row set
        """
        d = {}
        for key in row.keys():
            d[key] = row[key]
        return d
