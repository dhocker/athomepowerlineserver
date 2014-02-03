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

#
# main
#
if __name__ == "__main__":
  # First things, First
  disclaimer.Disclaimer.DisplayDisclaimer()
  print "Use ctrl-c to shutdown server\n"

  # Load the configuration file
  #Configuration.Configuration()
  Configuration.Configuration.LoadConfiguration()

  # Activate logging to console or file
  Logging.EnableLogging()

  logging.info("Starting up...")

  logging.info("X10 controller: %s", Configuration.Configuration.X10ControllerDevice())
  logging.info("ComPort: %s", Configuration.Configuration.ComPort())
  
  # Inject the X10 controller driver
  driver = Configuration.Configuration.GetX10ControllerDriver()
  drivers.X10ControllerAdapter.X10ControllerAdapter.Open(driver)

  # Initialize the database
  logging.info("Initializing database")
  database.AtHomePowerlineServerDb.AtHomePowerlineServerDb.Initialize()
  logging.info("Loading timer programs")
  timers.TimerStore.TimerStore.LoadTimerProgramList()
  
  #HOST, PORT = "localhost", 9999
  #HOST, PORT = "hedwig", 9999
  # This accepts connections from any network interface. It was the only
  # way to get it to work in the RPi from remote machines.
  HOST, PORT = "0.0.0.0", Configuration.Configuration.Port()

  # Fire up the timer service - watches for timer events to occur
  timer_service = services.TimerService.TimerService()
  timer_service.Start()
  logging.info("Timer service started")

  # Create the server, binding to localhost on port 9999
  #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandlerStream)
  ThreadedTCPServer.ThreadedTCPServer.allow_reuse_address = True
  server = ThreadedTCPServer.ThreadedTCPServer((HOST, PORT), MyTCPHandlerJson.MyTCPHandlerJson)

  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  logging.info("AtHomePowerlineServer now serving sockets at %s:%s", HOST, PORT)
  
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    logging.info("AtHomePowerlineServer shutting down...")
  except Exception as e: 
    logging.error("Unhandled exception occurred")
    logging.error(e.strerror)
    logging.error(sys.exc_info()[0])
  finally:
    timer_service.Stop()
    server.shutdown()
    drivers.X10ControllerAdapter.X10ControllerAdapter.Close()
    logging.info("AtHomePowerlineServer shutdown complete")