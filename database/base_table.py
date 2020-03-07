#
# Base table model for all database models
# Copyright © 2019, 2020  Dave Hocker
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
    # Error codes
    SUCCESS = 0
    BAD_REQUEST = 400
    SERVER_ERROR = 500

    @property
    def last_error_code(self):
        return self._last_error_code

    @last_error_code.setter
    def last_error_code(self, v):
        self._last_error_code = v

    @property
    def last_error(self):
        return self._last_error

    @last_error.setter
    def last_error(self, v):
        self._last_error = v

    def set_last_error(self, code, message):
        self.last_error_code = code
        self.last_error = message

    def clear_last_error(self):
        """
        Clear out the last error properties
        :return:
        """
        self.last_error_code = BaseTable.SUCCESS
        self.last_error = None

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
