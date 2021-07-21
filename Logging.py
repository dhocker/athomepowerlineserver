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
import logging.handlers
import os
import Configuration


########################################################################
# Enable logging for the AtHomePowerlineServer application
# TODO In order to get dual logging to work, we'll need to create
# a logger instance in every module that logs. We can configure that
# instance here. In the mean time, we'll use logging to file.
def EnableServerLogging():
    # Default overrides
    logformat = '%(asctime)s, %(module)s, %(levelname)s, %(message)s'
    logdateformat = '%Y-%m-%d %H:%M:%S'

    # Remove any existing configuration. However, this results in
    # output to the console. To avoid this, we send it to the null device.
    try:
        null_dev = open(os.devnull, 'w')
        logging.basicConfig(force=True, format=logformat, datefmt=logdateformat, stream=null_dev)
    except Exception as ex:
        # This isn't a terminal error, but we need to let it be known
        print("Unable to reset basic logging config")
        print(str(ex))

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

    # Configure the root logger to cover all loggers
    logger = logging.getLogger()
    logger.setLevel(loglevel)

    formatter = logging.Formatter(logformat, datefmt=logdateformat)

    # Do we log to console?
    if Configuration.Configuration.Logconsole():
        # Covers the server and pyHS100 package
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)
        ch.setFormatter(formatter)
        # logger.addHandler(ch)
        logger.addHandler(ch)

    # Do we log to a file?
    logfile = Configuration.Configuration.Logfile()
    if logfile != "":
        # To file
        fh = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', backupCount=3)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.debug("Logging to file: %s", logfile)


# Controlled logging shutdown
def Shutdown():
    logging.shutdown()
    print("Logging shutdown")
