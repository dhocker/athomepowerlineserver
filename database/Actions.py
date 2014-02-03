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
# Actions table model
#

import AtHomePowerlineServerDb
import datetime
import logging

#######################################################################
class Actions:
  
  #######################################################################
  def __init__(self):
    pass

  #######################################################################
  # Empty all records from the Actions table
  @classmethod
  def DeleteAll(cls):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
    c.execute("DELETE FROM Actions")
    conn.commit()
    conn.close()    

  #######################################################################
  # Return the set of all records in the Actions table
  @classmethod
  def GetAll(cls):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
    rset = c.execute("SELECT * from Actions")
    return rset

  #######################################################################
  # Return the record for a given action name
  # The return value is an Sqlite3 Row type
  @classmethod
  def GetByName(cls, name):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
    rset = c.execute("SELECT * from Actions where name=:name", {"name": name})
    return rset.fetchone()

  #######################################################################
  # Insert a record into the Actions table.
  # This is not exactly optimized, but we don't expect to be saving that many actions.
  @classmethod
  def Insert(cls, name, command, dim_amount, args):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
    # SQL insertion safe...
    # Note that the current time is inserted as the update time. This is added to the 
    # row as a convenient way to know when the timer was stored. It isn't used for
    # any other purpose.
    c.execute("INSERT INTO Actions values (?, ?, ?, ?, ?)", (name, command, dim_amount, args, datetime.datetime.now()))
    conn.commit()
    conn.close()

  #######################################################################
  # Debug: Dump all actions
  @classmethod
  def DumpActions(cls):
    logging.info("Actions Dump")
    rset = cls.GetAll()
    for r in rset:
      logging.info("Action: %s %s %s %s", r["name"], r["command"], r["dimamount"], r["updatetime"])
