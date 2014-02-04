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

import logging
import Configuration

########################################################################
# Enable logging for the AtHomePowerlineServer application
def EnableLogging():
  # Default overrides
  logformat = '%(asctime)s, %(levelname)s, %(message)s'
  logdateformat = '%Y-%m-%d %H:%M:%S'

  # Logging level override
  log_level_override = Configuration.Configuration.LogLevel().lower()
  if log_level_override == "debug":
    loglevel = logging.DEBUG
  elif log_level_override == "info":
    loglevel = logging.INFO
  elif log_level_override == "warn":
    loglevel = logging.WARNING
  elif log_level_override == "error":
    loglevel = logging.ERROR
  else:
    loglevel = logging.DEBUG

  # Do we log to a file or to the console?
  logfile = Configuration.Configuration.Logfile()
  if logfile != "":
    # To file
    logging.basicConfig(filename=logfile, level=loglevel, format=logformat, datefmt=logdateformat)
    logging.info("Logging to file: %s", logfile)
  else:
    # To console
    logging.basicConfig(level=loglevel, format=logformat, datefmt=logdateformat)
    logging.info("Logging to console")

