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
# Sunrise/sunset data access (sun_table in the AtHomePowerlineServer database)
#

import sqlite3
import os.path
import datetime
import time
import io
import glob
import AtHomePowerlineServerDb

SUN_DATA_FILE_NAME = "sunrise_sunset.sql"


def load_sun_table(conn):
  """
  Load the sun_table with all sunrise_sunset files
  """

  # Open access to DB
  csr = conn.cursor()

  #print "Loading file...", file
  fh = open(SUN_DATA_FILE_NAME)

  count = 0
  sql = fh.readline()
  while sql != "":
    csr.execute(sql)
    sql = fh.readline()
    count += 1
    #if count % 10 == 0:
    #  print count

  # One commit, after all records are inserted (much faster!)
  conn.commit()

  #print "All records loaded"


def get_sunrise(for_date):
  """
  Return the sunrise time for a given date
  """
  conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
  csr = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
  rst = csr.execute("select sunrise from sun_table where calendar_date=date(?)", [for_date.isoformat()])
  r = rst.fetchone()
  sunrise_without_date = datetime.datetime.strptime(r["sunrise"], "%H:%M:%S")
  sunrise_with_date = datetime.datetime(for_date.year, for_date.month, for_date.day, \
                                        sunrise_without_date.hour, sunrise_without_date.minute, sunrise_without_date.second)

  # Adjustment for DST (database times are ALL in STD time)
  if time.localtime().tm_isdst:
    sunrise_with_date += datetime.timedelta(hours=1)

  return sunrise_with_date


def get_sunset(for_date):
  """
  Return the sunset time for a given date
  """
  conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
  csr = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetCursor(conn)
  rst = csr.execute("select sunset from sun_table where calendar_date=date(?)", [for_date.isoformat()])
  r = rst.fetchone()
  sunset_without_date = datetime.datetime.strptime(r["sunset"], "%H:%M:%S")
  sunset_with_date = datetime.datetime(for_date.year, for_date.month, for_date.day, \
                                        sunset_without_date.hour, sunset_without_date.minute, sunset_without_date.second)

  # Adjustment for DST (database times are ALL in STD time)
  if time.localtime().tm_isdst:
    sunset_with_date += datetime.timedelta(hours=1)

  return sunset_with_date

#
# Run application
#
if __name__ == "__main__":
  # If the database already exists, we'll reload the sun_table.
  # Otherwise, we'll create a new database and load the sun_table
  if os.path.exists(AtHomePowerlineServerDb.AtHomePowerlineServerDb.DatabaseFileName):
    conn = AtHomePowerlineServerDb.AtHomePowerlineServerDb.GetConnection()
    load_sun_table(conn)
  else:
    AtHomePowerlineServerDb.AtHomePowerlineServerDb.CreateDatabase()

