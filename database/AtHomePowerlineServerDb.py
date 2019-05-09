# -*- coding: utf-8 -*-
#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright © 2014, 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# AtHomePowerlineServer database
#

import sqlite3
import os.path
import datetime
import logging
import Configuration

logger = logging.getLogger("server")


#######################################################################
class AtHomePowerlineServerDb:
    DatabaseFileName = "AtHomePowerlineServer.sqlite3"

    def __init__(self):
        pass

    #######################################################################
    @classmethod
    def Initialize(cls):
        if os.path.isfile(Configuration.Configuration.GetDatabaseFilePath(cls.DatabaseFileName)):
            # Database exists
            logger.info("Using database file: %s",
                        Configuration.Configuration.GetDatabaseFilePath(cls.DatabaseFileName))
        else:
            # Database needs to be created
            cls.CreateDatabase()
            logger.info("Created database file: %s",
                        Configuration.Configuration.GetDatabaseFilePath(cls.DatabaseFileName))

    #######################################################################
    # Create a new database
    # There is no way to migrate a database. When schema changes are
    # required, it is expected that the old database will be deleted
    # and a new database created. Then, the timers and actions can
    # be reloaded. This choice was made just to keep things simple.
    # In the future, if something more sophisticated is warranted,
    # it can be implemented at that time.
    @classmethod
    def CreateDatabase(cls):
        # This actually creates the database if it does not exist
        # Note that the return value is a connection object
        conn = cls.GetConnection()

        # Create tables (Sqlite3 specific)
        # SchemaVersion (sort of the migration version)
        conn.execute("CREATE TABLE SchemaVersion (Version text, updatetime timestamp)")
        conn.execute("INSERT INTO SchemaVersion values (?, ?)", ("4.0.0.0", datetime.datetime.now()))
        conn.commit()

        # Timers
        conn.execute("CREATE TABLE Timers (name text PRIMARY KEY, deviceid integer, daymask text, \
      starttriggermethod text, starttime timestamp, startoffset integer, \
      startrandomize integer, startrandomizeamount integer, \
      stoptriggermethod text, stoptime timestamp, stopoffset integer, \
      stoprandomize integer, stoprandomizeamount integer, \
      startaction text, stopaction text, security integer, updatetime timestamp)")

        # Actions
        conn.execute(
            "CREATE TABLE Actions (name text PRIMARY KEY, command text, dimamount integer, args text, updatetime timestamp)")

        # Devices
        # Note that by definition Sqlite treats the id columns as the ROWID. See https://www.sqlite.org/autoinc.html
        conn.execute(
            "CREATE TABLE Devices (id integer PRIMARY KEY, name text, location text, \
            type text, address text, selected integer, updatetime timestamp)")

        # Done
        conn.close()

    #######################################################################
    # Returns a database connection
    @classmethod
    def GetConnection(cls):
        conn = sqlite3.connect(Configuration.Configuration.GetDatabaseFilePath(cls.DatabaseFileName))
        # We use the row factory to get named row columns. Makes handling row sets easier.
        conn.row_factory = sqlite3.Row
        # The default string type is unicode. This changes it to UTF-8.
        conn.text_factory = str
        return conn

    #######################################################################
    @classmethod
    def GetCursor(cls, conn):
        return conn.cursor()
