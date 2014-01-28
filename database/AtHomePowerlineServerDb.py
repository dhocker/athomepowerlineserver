#
# AtHomePowerlineServer database
#

import sqlite3
import os.path

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
    c.execute("CREATE TABLE Timers (name text, housedevicecode text, daymask text, ontime timestamp, offtime timestamp, \
      security integer, updatetime timestamp)")

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