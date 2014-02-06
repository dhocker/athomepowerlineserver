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
  logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
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

  EnableServerLogging()

########################################################################
# Enable logging for the AtHomePowerlineServer application
# TODO In order to get dual logging to work, we'll need to create
# a logger instance in every module that logs. We can configure that
# instance here. In the mean time, we'll use logging to file.
def EnableLogging2():
  # Default overrides
  logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
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

  logger = logging.getLogger()

  # Do we log to a file?
  logfile = Configuration.Configuration.Logfile()
  if logfile != "":
    # To file
    fh = logging.FileHandler(logfile)
    fh.setLevel(loglevel)
    fh.setFormatter(logformat)
    #logger.addHandler(fh)
    #logging.info("Logging to file: %s", logfile)
  else:
    fh = None

  # To console
  ch = logging.StreamHandler()
  ch.setLevel(loglevel)
  ch.setFormatter(logformat)
  #logger.addHandler(ch)
  #logging.info("Logging to console")

  if fh is None:
    logging.basicConfig(level=loglevel, handlers=[ch])
  else:
    logging.basicConfig(level=loglevel, handlers=[fh])

########################################################################
# Enable logging for the AtHomePowerlineServer application
# TODO In order to get dual logging to work, we'll need to create
# a logger instance in every module that logs. We can configure that
# instance here. In the mean time, we'll use logging to file.
def EnableServerLogging():
  # Default overrides
  logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
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

  logger = logging.getLogger("server")
  logger.setLevel(loglevel)

  formatter = logging.Formatter(logformat, datefmt=logdateformat)

  # To console
  ch = logging.StreamHandler()
  ch.setLevel(loglevel)
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  # Do we log to a file?
  logfile = Configuration.Configuration.Logfile()
  if logfile != "":
    # To file
    fh = logging.FileHandler(logfile)
    fh.setLevel(loglevel)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.debug("Logging to file: %s", logfile)

  logger.debug("Logging to console")

# Controlled logging shutdown
def Shutdown():
  logging.shutdown()
  print "Logging shutdown"