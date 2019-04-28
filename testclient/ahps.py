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
# Command line tool for AtHomePowerlineServer
#
# ahps.py [-s hostname|hostaddress] [-p portnumber] [-d dimamount] command house/device-code
#
# Commands and operands
#   applianceon house-code
#   applianceoff house-code
#   lampoff house-code
#   deviceoff house-code
#   lampon house-code dim-amount
#

import testclient.ahps_client
import argparse
import sys

#######################################################################
#
# Main
#
if __name__ == "__main__":
    # Show license advertisement
    sys.path.append("../")
    import disclaimer.Disclaimer

    disclaimer.Disclaimer.DisplayDisclaimer()

    # Turn off verbose result reporting in the client API
    testclient.ahps_client.Verbose = False

    # import pdb; pdb.set_trace()

    # Create an argument parser for the optional and positional arguments
    parser = argparse.ArgumentParser(description="ahps - AtHomePowerlineServer command line utility")
    parser.add_argument("command", help="X10 command: applianceon, lampon, applianceoff, lampoff, deviceoff")
    parser.add_argument("housedevicecode", help="House device code (e.g. A7)")
    parser.add_argument("-s", "--server", help="Host name or host address")
    parser.add_argument("-p", "--port", type=int, help="Port number")
    parser.add_argument("-d", "--dimamount", type=int, default=0,
                        help="For lamp module commands, the dim amount. Default=0")
    args = parser.parse_args()

    # Local default is the localhost
    testclient.ahps_client.Host = "localhost"
    if args.server is not None:
        testclient.ahps_client.Host = args.server
    if args.port is not None:
        testclient.ahps_client.Port = args.port

    # Try a status request command
    response = testclient.ahps_client.StatusRequest()
    # Make sure we received a good response
    rc = response["result-code"]
    if rc != 0:
        print("StatusRequest failed with result-code ", rc)
        exit()

    # Command parsing
    cmd = args.command.lower()
    response = None
    if cmd == "applianceon":
        response = testclient.ahps_client.DeviceOn(args.housedevicecode, 0)
    elif cmd == "lampon":
        response = testclient.ahps_client.DeviceOn(args.housedevicecode, args.dimamount)
    elif cmd == "applianceoff" or cmd == "deviceoff":
        response = testclient.ahps_client.DeviceOff(args.housedevicecode, 0)
    elif cmd == "lampoff":
        response = testclient.ahps_client.DeviceOff(args.housedevicecode, args.dimamount)
    else:
        print("Unrecognized command: ", cmd)
        parser.print_help()

    # Report results
    if response is not None:
        print("Result code: ", response["result-code"])
    else:
        print("Command did not return a response")
