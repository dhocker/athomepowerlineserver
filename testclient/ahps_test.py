#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Test client for AtHomePowerlineServer
#
# ahps_test.py [-s hostname|hostaddress] [-p portnumber]
#

import sys
import time
import ahps_client
from optparse import OptionParser

#######################################################################
#
# Main
#
if __name__ == "__main__":
    # Show license advertisement
    sys.path.append("../")
    import disclaimer.Disclaimer

    disclaimer.Disclaimer.DisplayDisclaimer()

    # import pdb; pdb.set_trace()

    parser = OptionParser()
    parser.add_option("-s")
    parser.add_option("-p")
    (options, args) = parser.parse_args()
    # print options

    if options.s is not None:
        Host = options.s
    if options.p is not None:
        Port = int(options.p)

    # Try a status request command
    ahps_client.StatusRequest()

    # Test the time requests
    # SetTime()
    # GetTime()

    # Try some timer programs
    # LoadTimers()

    # LoadActions()

    print("A7 on 50")
    ahps_client.DeviceOn("A7", 50)
    #
    print("sleep 10")
    time.sleep(10)
    #
    print("A7 bright 50")
    ahps_client.DeviceBright("a7", 50)
    #
    # print "A7 dim 50"
    # ahps_client.DeviceDim("A7", 50)
    #
    # print "sleep 5"
    # time.sleep(5)
    #
    # print "A7 off"
    # ahps_client.DeviceOff("A7", 0)

    print("sleep 10")
    time.sleep(10)

    print("All units off A")
    ahps_client.DeviceAllUnitsOff("A")
    # print "All units off P"
    # ahps_client.DeviceAllUnitsOff("P")

    # print "All lights off"
    # ahps_client.DeviceAllLightsOff("A")
