#
# Devices table model
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from database.AtHomePowerlineServerDb import AtHomePowerlineServerDb
from .base_table import BaseTable
import datetime
import logging

logger = logging.getLogger("server")


class Devices(BaseTable):
    TPLINK = "tplink"
    X10 = "x10"
    # All valid device types and the device type class they belong to
    VALID_DEVICE_LIST = {
        "x10": X10,
        "x10-appliance": X10,
        "x10-lamp": X10,
        "tplink": TPLINK,
        "hs100": TPLINK,
        "hs103": TPLINK,
        "hs105": TPLINK,
        "hs107": TPLINK,
        "hs110": TPLINK,
        "hs200": TPLINK,
        "hs210": TPLINK,
        "hs220": TPLINK,
        "smartplug": TPLINK,
        "smartswitch": TPLINK,
        "smartbulb": TPLINK
    }

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
    def get_all_devices(cls):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        # The results are sorted based on the most probable use
        rset = c.execute("SELECT * from Devices ORDER BY location, name")
        return cls.rows_to_dict_list(rset)

    @classmethod
    def get_device(cls, device_id):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute("SELECT * from Devices WHERE id=:deviceid", {"deviceid": device_id})
        return cls.row_to_dict(rset.fetchone())

    @classmethod
    def insert(cls, device_name, device_location, device_type, device_address, device_selected):
        """
        Insert a new device record
        :param device_name: name/tag/label for the device (human readable)
        :param device_location: location of device in house
        :param device_type: device type (e.g. x10, tplink, hs100, etc.)
        :param device_address: x10 house-device-code or ip address or ...
        :param device_selected: device is selected for "all selected" action
        :return:
        """
        if not cls.is_valid_device_type(device_type):
            return -1

        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        # SQL insertion safe...
        # Note that the current time is inserted as the update time. This is added to the
        # row as a convenient way to know when the record was inserted. It isn't used for
        # any other purpose.
        c.execute("INSERT INTO Devices (name,location,type,address,selected,updatetime) values (?,?,?,?,?,?)",
                  (device_name, device_location, device_type, device_address, device_selected, datetime.datetime.now()))
        id = c.lastrowid
        conn.commit()
        conn.close()
        return id

    @classmethod
    def update(cls, device_id, device_name, device_location, device_type, device_address, device_selected):
        """
        Update an existing device record
        :param device_id: ID of existing device
        :param device_name: name/tag/label for the device (human readable)
        :param device_location: location of device in house
        :param device_type: device type (e.g. x10, tplink, hs100, etc.)
        :param device_address: x10 house-device-code or ip address or ...
        :param device_selected: device is selected for "all selected" action
        :return:
        """
        if not cls.is_valid_device_type(device_type):
            return False

        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        # SQL update safe...
        # Note that the current time is inserted as the update time. This is added to the
        # row as a convenient way to know when the record was inserted. It isn't used for
        # any other purpose.
        c.execute("UPDATE Devices SET " \
                    "name=?,location=?,type=?,address=?,selected=?,updatetime=? WHERE id=?",
                    (device_name, device_location, device_type, device_address, device_selected,
                    datetime.datetime.now(), device_id)
                  )
        conn.commit()
        change_count = conn.total_changes
        conn.close()
        return change_count

    @classmethod
    def delete_device(cls, device_id):
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Devices WHERE id=:deviceid", {"deviceid": device_id})
        conn.commit()
        change_count = conn.total_changes
        conn.close()
        return change_count

    @classmethod
    def get_device_by_id(cls, device_id):
        """
        Return the dvice record for a given device
        :param device_id: The device id (key)
        :return: device record as a dict
        """
        conn = AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.GetCursor(conn)
        rset = c.execute("SELECT * from Devices where id=:id", {"id": device_id})
        return cls.row_to_dict(rset.fetchone())

    @classmethod
    def is_valid_device_type(cls, device_type):
        return device_type.lower() in cls.VALID_DEVICE_LIST.keys()