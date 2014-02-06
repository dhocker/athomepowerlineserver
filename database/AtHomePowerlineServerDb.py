#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker
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

logger = logging.getLogger("server")

#######################################################################
class AtHomePowerlineServerDb:

  DatabaseFileName = "AtHomePowerlineServer.sqlite3"

  def __init__(self):
    pass

  #######################################################################
  @classmethod
  def Initialize(cls):

    if os.path.isfile(cls.DatabaseFileName):
      # Database exists
      pass
    else:
      # Database needs to be created
      cls.CreateDatabase()
      logger.info("Created database file: %s", cls.DatabaseFileName)

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
    # Note that the return value is a cursor object
    csr = cls.GetConnection()

    # Create tables (Sqlite3 specific)
    # SchemaVersion (sort of the migration version)
    csr.execute("CREATE TABLE SchemaVersion (Version text, updatetime timestamp)")
    csr.execute("INSERT INTO SchemaVersion values (?, ?)", ("1.0.0.0", datetime.datetime.now()))
    # Timers
    csr.execute("CREATE TABLE Timers (name text PRIMARY KEY, housedevicecode text, daymask text, starttime timestamp, stoptime timestamp, \
      startaction text, stopaction text, security integer, updatetime timestamp)")
    # Actions
    csr.execute("CREATE TABLE Actions (name text PRIMARY KEY, command text, dimamount integer, args text, updatetime timestamp)")

    # Done
    csr.close()

  #######################################################################
  # Returns a database connection
  @classmethod
  def GetConnection(cls):
    conn = sqlite3.connect(cls.DatabaseFileName)
    # We use the row factory to get named row columns. Makes handling row sets easier.
    conn.row_factory = sqlite3.Row
    # The default string type is unicode. This changes it to UTF-8.
    conn.text_factory = str
    return conn

  #######################################################################
  @classmethod
  def GetCursor(cls, conn):
    return conn.cursor()