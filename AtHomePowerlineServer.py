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
import socket
import drivers.X10ControllerAdapter
import database.AtHomePowerlineServerDb
import timers.TimerStore
import services.TimerService
import disclaimer.Disclaimer

#
# main
#
if __name__ == "__main__":
  # First things, First
  disclaimer.Disclaimer.DisplayDisclaimer()

  print "Starting up..."

  # Load the configuration file
  #Configuration.Configuration()
  Configuration.Configuration.LoadConfiguration()
  
  print "X10 controller:", Configuration.Configuration.X10ControllerDevice()
  print "ComPort:", Configuration.Configuration.ComPort()
  
  # Inject the X10 controller driver
  driver = Configuration.Configuration.GetX10ControllerDriver()
  drivers.X10ControllerAdapter.X10ControllerAdapter.Open(driver)

  # Initialize the database
  print "Initializing database"
  database.AtHomePowerlineServerDb.AtHomePowerlineServerDb.Initialize()
  print "Loading timer programs"
  timers.TimerStore.TimerStore.LoadTimerProgramList()
  
  #HOST, PORT = "localhost", 9999
  #HOST, PORT = "hedwig", 9999
  # This accepts connections from any network interface. It was the only
  # way to get it to work in the RPi from remote machines.
  HOST, PORT = "0.0.0.0", Configuration.Configuration.Port()

  # Fire up the timer service - watches for timer events to occur
  timer_service = services.TimerService.TimerService()
  timer_service.Start()
  print "Timer service started"

  # Create the server, binding to localhost on port 9999
  #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandlerStream)
  ThreadedTCPServer.ThreadedTCPServer.allow_reuse_address = True
  server = ThreadedTCPServer.ThreadedTCPServer((HOST, PORT), MyTCPHandlerJson.MyTCPHandlerJson)

  # Activate the server; this will keep running until you
  # interrupt the program with Ctrl-C
  print "AtHomePowerlineServer now serving sockets at {0}:{1}...".format(HOST, PORT)
  
  try:
    print "Use ctrl-c to shutdown server"
    server.serve_forever()
  except KeyboardInterrupt:
    print "\n"
    print "AtHomePowerlineServer shutting down..."
  except Exception as e: 
    print "Unhandled exception occurred\n"
    print e.strerror
    print sys.exc_info()[0]
  finally:
    timer_service.Stop()
    server.shutdown()
    drivers.X10ControllerAdapter.X10ControllerAdapter.Close()
    print "AtHomePowerlineServer shutdown complete"