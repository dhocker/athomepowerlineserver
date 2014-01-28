#
# Timers table model
#

import AtHomePowerlineServerDb
import datetime

#######################################################################
class Timers:
  
  #######################################################################
  def __init__(self):
    pass

  #######################################################################
  # Empty all records from the Timers table
  @classmethod
  def DeleteAll(cls):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
    c.execute("DELETE FROM Timers")
    conn.commit()
    conn.close()    

  #######################################################################
  # Return the set of all records in the Timers table
  @classmethod
  def GetAll(cls):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
    rset = c.execute("SELECT * from Timers")
    return rset

  #######################################################################
  # Insert a record into the Timers table.
  # This is not exactly optimized, but we don't expect to be saving that many timer programs.
  @classmethod
  def Insert(cls, name, house_device_code, day_mask, on_time, off_time, security):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    c = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
    # SQL insertion safe...
    # Note that the current time is inserted as the update time. This is added to the 
    # row as a convenient way to know when the timer was stored. It isn't used for
    # any other purpose.
    c.execute("INSERT INTO Timers values (?, ?, ?, ?, ?, ?, ?)", (name, house_device_code, day_mask, \
      on_time, off_time, security, datetime.datetime.now()))
    conn.commit()
    conn.close()