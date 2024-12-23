#!/usr/bin/python

#
# AtHomePowerlineServer - networked server for remote power controlled devices
# Copyright © 2014, 2020  Dave Hocker (email: AtHomeX10@gmail.com)
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

import SocketServerThread
import Configuration
import Logging
from drivers.device_driver_manager import DeviceDriverManager
import database.AtHomePowerlineServerDb
import services.TimerService
import disclaimer.Disclaimer
import logging
import signal
import os
import pwd
import time
import sys
import ntplib


#
# main
#
def main():
    logger = logging.getLogger("server")

    # Clean up when killed
    def term_handler(signum, frame):
        logger.info("AtHomePowerlineServer received kill signal...shutting down")
        # This will break the forever loop at the foot of main()
        terminate_service = True
        sys.exit(0)

    # Orderly clean up of the server
    def CleanUp():
        timer_service.Stop()
        server.Stop()
        DeviceDriverManager.close_drivers()
        logger.info("AtHomePowerlineServer shutdown complete")
        logger.info("################################################################################")
        Logging.Shutdown()

    # Change the current directory so we can find the configuration file.
    # For Linux we should probably put the configuration file in the /etc directory.
    just_the_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(just_the_path)

    # Load the configuration file
    if not Configuration.Configuration.load_configuration():
        exit(1)

    # Per GPL, show the disclaimer
    disclaimer.Disclaimer.DisplayDisclaimer()
    print("Use ctrl-c to shutdown server\n")

    # Activate logging to console or file
    # Logging.EnableLogging()
    Logging.EnableServerLogging()

    logger.info("################################################################################")

    # For additional coverage, log the disclaimer
    disclaimer.Disclaimer.LogDisclaimer()

    current_user = pwd.getpwuid(os.getuid()).pw_name
    logger.info(f"Starting up under user {current_user}...")

    logger.info("Using configuration file: %s", Configuration.Configuration.GetConfigurationFilePath())

    # Verify Internet access. This is required for Meross devices to work.
    # This is mostly about recovering from power outages.
    logger.info("Verifying Internet connection...")
    ntp_client = ntplib.NTPClient()
    while True:
        try:
            # Internet access is verified by connecting to a reliable, well-known
            # server (in this case an NTP server).
            response = ntp_client.request("time.nist.gov")
            if response is not None:
                logger.info("Internet verification successful")
                break
            time.sleep(5.0)
        except KeyboardInterrupt:
            logger.info("AtHomePowerlineServer shutting down after Internet verification failed...")
            exit(999)
        except ntplib.NTPException:
            # Wait 5 sec and try again
            time.sleep(5.0)
        except Exception as e:
            logger.error("Unhandled exception occurred during Internet verification")
            logger.error(str(e))
            # logger.error(sys.exc_info()[0])
            time.sleep(5.0)

    # Create drivers for all supported devices/manufacturers
    DeviceDriverManager.init()

    # Initialize the database
    logger.info("Initializing database")
    database.AtHomePowerlineServerDb.AtHomePowerlineServerDb.Initialize()

    # HOST, PORT = "localhost", 9999
    # HOST, PORT = "hedwig", 9999
    # This accepts connections from any network interface. It was the only
    # way to get it to work in the RPi from remote machines.
    HOST, PORT = "0.0.0.0", Configuration.Configuration.Port()

    # Fire up the timer service - watches for timer events to occur
    timer_service = services.TimerService.TimerService()
    timer_service.Start()
    logger.info("Timer service started")

    # Create the TCP socket server on its own thread.
    # This is done so that we can handle the kill signal which
    # arrives on the main thread. If we didn't put the TCP server
    # on its own thread we would not be able to shut it down in
    # an orderly fashion.
    server = SocketServerThread.SocketServerThread(HOST, PORT)

    # Set up handler for the kill signal
    signal.signal(signal.SIGTERM, term_handler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C or kill the daemon.

    # Launch the socket server
    try:
        # This runs "forever", until ctrl-c or killed
        server.Start()
        terminate_service = False
        while not terminate_service:
            # We do a lot of sleeping to avoid using too much CPU :-)
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("AtHomePowerlineServer shutting down...")
    except Exception as e:
        logger.error("Unhandled exception occurred")
        logger.error(e.strerror)
        logger.error(sys.exc_info()[0])
    finally:
        # We actually get here through ctrl-c or process kill (SIGTERM)
        CleanUp()


#
# Run as an application or daemon
#
if __name__ == "__main__":
    main()
