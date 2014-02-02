#
# AtHomPowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
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
      print "Created database file:", cls.DatabaseFileName

  #######################################################################
  @classmethod
  def CreateDatabase(cls):
    # This actually creates the database if it does not exist
    # Note that the return value is a cursor object
    c = cls.GetConnection()

    # Create tables
    # SchemaVersion
    c.execute("CREATE TABLE SchemaVersion (Version text, updatetime timestamp)")
    c.execute("INSERT INTO SchemaVersion values (?, ?)", ("1.0.0.0", datetime.datetime.now()))
    # Timers
    c.execute("CREATE TABLE Timers (name text, housedevicecode text, daymask text, starttime timestamp, stoptime timestamp, \
      security integer, updatetime timestamp)")
    # Actions
    c.execute("CREATE TABLE Actions (name text, command text, dimamount integer, args text, updatetime timestamp)")

    # Done
    c.close()

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