#
# Base table model for all database models
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


class BaseTable:
    @classmethod
    def rows_to_dict_list(cls, rows):
        """
        Convert a list of SQLite rows to a list of dicts
        :param rows: SQLite row set to be converted
        :return:
        """
        dl = []
        for row in rows.fetchall():
            dl.append(cls.row_to_dict(row))
        return dl

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
