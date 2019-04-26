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

import database.AtHomePowerlineServerDb as AtHomePowerlineServerDb
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
    def DeleteAll(cls):
        conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
        c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
        c.execute("DELETE FROM Timers")
        conn.commit()
        conn.close()
