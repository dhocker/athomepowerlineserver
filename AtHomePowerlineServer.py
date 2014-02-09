#!/usr/bin/python

#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

import ThreadedTCPServer
import MyTCPHandlerJson
import Configuration
import Logging
import drivers.X10ControllerAdapter
import database.AtHomePowerlineServerDb
import timers.TimerStore
import services.TimerService
import disclaimer.Disclaimer
import logging
import signal
import os

#
# main
#
def main():
  logger = logging.getLogger("server")

  # Clean up when killed
  def term_handler(signum, frame):
    logger.info("AtHomePowerlineServer received kill signal")
    CleanUp()

  # Order clean up of the server
  def CleanUp():
    timer_service.Stop()
    server.shutdown()
    drivers.X10ControllerAdapter.X10ControllerAdapter.Close()
    logger.info("AtHomePowerlineServer shutdown complete")
    logger.info("################################################################################")
    Logging.Shutdown()

  # First things, First
  disclaimer.Disclaimer.DisplayDisclaimer()
  print "Use ctrl-c to shutdown server\n"

  # Change the current directory so we can find the configuration file.
  # For Linux we should probably put the configuration file in the /etc directory.
  just_the_path = os.path.dirname(os.path.realpath(__file__))
  os.chdir(just_the_path)

  # Load the configuration file
  Configuration.Configuration.LoadConfiguration()

  # Activate logging to console or file
  # Logging.EnableLogging()
  Logging.EnableServerLogging()

  logger.info("################################################################################")
  logger.info("Starting up...")

  logger.info("X10 controller: %s", Configuration.Configuration.X10ControllerDevice())
  logger.info("ComPort: %s", Configuration.Configuration.ComPort())

  # Inject the X10 controller driver
  driver = Configuration.Configuration.GetX10ControllerDriver()
  drivers.X10ControllerAdapter.X10ControllerAdapter.Open(driver)

  # Initialize the database
  logger.info("Initializing database")
  database.AtHomePowerlineServerDb.AtHomePowerlineServerDb.Initialize()
  logger.info("Loading timer programs")
  timers.TimerStore.TimerStore.LoadTimerProgramList()

  #HOST, PORT = "localhost", 9999
  #HOST, PORT = "hedwig", 9999
  # This accepts connections from any network interface. It was the only
  # way to get it to work in the RPi from remote machines.
  HOST, PORT = "0.0.0.0", Configuration.Configuration.Port()

  # Fire up the timer service - watches for timer events to occur
  timer_service = services.TimerService.TimerService()
  timer_service.Start()
  logger.info("Timer service started")

  # Create the server, binding to localhost on port 9999
  #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandlerStream)
  ThreadedTCPServer.ThreadedTCPServer.allow_reuse_address = True
  server = ThreadedTCPServer.ThreadedTCPServer((HOST, PORT), MyTCPHandlerJson.MyTCPHandlerJson)

  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  logger.info("AtHomePowerlineServer now serving sockets at %s:%s", HOST, PORT)

  # Set up handle for the kill signal
  signal.signal(signal.SIGTERM, term_handler)

  # Launch the socket server
  try:
    # This runs "forever", until ctrl-c or killed
    server.serve_forever()
  except KeyboardInterrupt:
    logger.info("AtHomePowerlineServer shutting down...")
  except Exception as e:
    logger.error("Unhandled exception occurred")
    logger.error(e.strerror)
    logger.error(sys.exc_info()[0])
  finally:
    CleanUp()

#
# Run as an application
#
if __name__ == "__main__":
  main()