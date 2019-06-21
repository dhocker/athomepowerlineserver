#
# AtHomePowerlineServer - networked server for X10 and WiFi devices
# Copyright © 2014, 2019  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

#
# Test client for AtHomePowerlineServer and ahps API module
#
# python3 ahps_client.py [-s hostname|hostaddress] [-p portnumber] [-v | -q] request [arguments]
#

import sys
import json
from optparse import OptionParser
sys.path.append("./")
sys.path.append("../")
# from testclient.ahps import ServerRequest
from athomeapi import ServerRequest


# Default global settings
host = "localhost"
port = 9999
verbose = True


def _required_keys(dict_to_test, keys):
    """
    Test a dict for a list of required keys. Extra keys are ignored.
    :param dict_to_test:
    :param keys: list of keys that must be present
    :return: True if all keys are present
    """
    for key in keys:
        if key not in dict_to_test.keys():
            raise KeyError("Required key missing: " + key)
    return True


def _open_request(request_args):
    """
    An open server request. The argument is a JSON file
    containing the entire request. This is the "raw" interface.
    :param request_args: request request_file.json
    :return:
    """
    try:
        fh = open(args[1], "r")
        dev_json = json.load(fh)
        fh.close()
    except Exception as ex:
        print(str(ex))
        return None

    request = ServerRequest(host=host, port=port, verbose=verbose)
    result = request.open_request(dev_json)
    return result


def _device_on(request_args):
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.device_on(request_args[1], request_args[2])


def _device_off(request_args):
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.device_off(request_args[1], request_args[2])


def _device_dim(request_args):
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.device_dim(request_args[1], request_args[2])


def _device_bright(request_args):
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.device_bright(request_args[1], request_args[2])


def _status_request(request_args):
    # This DOES NOT work. Why?
    # data = "{ \"command\": \"StatusRequest\", \"args\": {\"a\": 1} }"

    # This DOES work. Why?
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.status_request()


def _create_timer_program(program):
    timer_program = {
        "name": program["name"],
        "device-id": str(program["device-id"]),
        "day-mask": program["day-mask"],
        "trigger-method": program["trigger-method"],
        "time": program["time"],
        "offset": str(program["offset"]),
        "command": program["command"],
        "randomize": True if program["randomize"] else False,
        "randomize-amount": str(program["randomize-amount"]),
        "dimamount": str(program["dimamount"])
    }
    return timer_program


def _define_program(request_args):
    dd_required_keys = [
        "name",
        "device-id",
        "day-mask",
        "trigger-method",
        "time",
        "offset",
        "command",
        "randomize",
        "randomize-amount",
        "dimamount"
    ]
    try:
        fh = open(args[1], "r")
        dev_json = json.load(fh)
        fh.close()
        # Test for required keys
        _required_keys(dev_json, dd_required_keys)
    except Exception as ex:
        print(str(ex))
        return None

    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.define_program(_create_timer_program(dev_json))


def _update_program(request_args):
    dd_required_keys = [
        "id",
        "name",
        "device-id",
        "day-mask",
        "trigger-method",
        "time",
        "offset",
        "command",
        "randomize",
        "randomize-amount",
        "dimamount"
    ]
    try:
        fh = open(args[1], "r")
        dev_json = json.load(fh)
        fh.close()
        # Test for required keys
        _required_keys(dev_json, dd_required_keys)
    except Exception as ex:
        print(str(ex))
        return None

    program = _create_timer_program(dev_json)
    program["id"] = dev_json["id"]

    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.update_program(program)


def _delete_program(request_args):
    """
    Delete a device program by program ID
    :param request_args:
    :return:
    """
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.delete_program(request_args[1])


def _define_device(request_args):
    dd_required_keys = [
        "device-name",
        "device-location",
        "device-type",
        "device-address",
        "device-selected"
    ]
    try:
        fh = open(args[1], "r")
        dev_json = json.load(fh)
        fh.close()
        # Test for required keys
        _required_keys(dev_json, dd_required_keys)
    except Exception as ex:
        print(str(ex))
        return None

    device = {}
    device["device-name"] = dev_json["device-name"]
    device["device-location"] = dev_json["device-location"]
    device["device-type"] = dev_json["device-type"]
    device["device-address"] = dev_json["device-address"]
    device["device-selected"] = dev_json["device-selected"]

    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.define_device(device)


def _update_device(request_args):
    dd_required_keys = [
        "device-id",
        "device-name",
        "device-location",
        "device-type",
        "device-address",
        "device-selected"
    ]
    try:
        fh = open(args[1], "r")
        dev_json = json.load(fh)
        # Test for required keys
        _required_keys(dev_json, dd_required_keys)
        fh.close()
    except Exception as ex:
        print(str(ex))
        return None

    device = {}
    device["device-id"] = dev_json["device-id"]
    device["device-name"] = dev_json["device-name"]
    device["device-location"] = dev_json["device-location"]
    device["device-type"] = dev_json["device-type"]
    device["device-address"] = dev_json["device-address"]
    device["device-selected"] = dev_json["device-selected"]

    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.update_device(device)


def _delete_device(request_args):
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.delete_device(request_args[1])


def _query_devices(request_args):
    """
    Query for all devices
    :param request_args:
    :return:
    """
    request = ServerRequest(host=host, port=port, verbose=verbose)
    if len(request_args) == 2:
        return request.query_device(request_args[1])
    return request.query_devices()


def _query_device_programs(request_args):
    """
    Query for all programs for a device ID
    :param request_args:
    :return:
    """
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.query_device_programs(request_args[1])


def _query_device_program(request_args):
    """
    Query for a device progam by its program ID
    :param request_args:
    :return:
    """
    request = ServerRequest(host=host, port=port, verbose=verbose)
    return request.query_device_program(request_args[1])


def _request_help(request_args):
    """
    help request
    :param request_args:
    :return:
    """
    print("Help - Request List")
    print("Legend")
    print("  All request names are case insensitive")
    print("  device-id is the unique identifier for a device")
    print("  program-id is the unique identifier for a program")
    print("  <filename.json> is a JSON formatted file")
    print()

    if request_args[1].lower() in ["*", "all"]:
        for key in request_list.keys():
            r = request_list[key]
            print(key)
            print("  Description:", r["description"])
            print("  Syntax:", r["syntax"])
    elif request_args[1].lower() in request_list.keys():
        r = request_list[request_args[1]]
        print(request_args[1])
        print("  Description:", r["description"])
        print("  Syntax:", r["syntax"])
    else:
        print(request_args[1], "is not a valid request")


"""
List of all supported requests

handler: the function that handles the request
argcount: the number of required request arguments including the request
"""
request_list = {
    "help": {
        "description": "Help for one or all requests",
        "syntax": "help [requestname | all]",
        "handler": _request_help,
        "argcount": 2
    },
    "statusrequest": {
        "description": "Returns the status of the server",
        "syntax": "StatusRequest",
        "handler": _status_request,
        "argcount": 1
    },
    "request": {
        "description": "A raw request in JSON format",
        "syntax": "request <request_file.json>",
        "handler": _open_request,
        "argcount": 2
    },
    "on": {
        "description": "Turn a device on",
        "syntax": "on device-id",
        "handler": _device_on,
        "argcount": 3
    },
    "deviceon": {
        "description": "Turn a device one",
        "syntax": "deviceon device-id",
        "handler": _device_on,
        "argcount": 3
    },
    "off": {
        "description": "Turn a device off",
        "syntax": "off device-id",
        "handler": _device_off,
        "argcount": 3
    },
    "deviceoff": {
        "description": "Turn a device off",
        "syntax": "deviceoff device-id",
        "handler": _device_off,
        "argcount": 3
    },
    "definedevice": {
        "description": "Define a new device using a JSON formatted input file",
        "syntax": "definedevice <new_device.json>",
        "handler": _define_device,
        "argcount": 2
    },
    "updatedevice": {
        "description": "Update a device definition using a JSON formatted input file",
        "syntax": "updatedevice <update_device.json>",
        "handler": _update_device,
        "argcount": 2
    },
    "deletedevice": {
        "description": "Delete a device by ID",
        "syntax": "deletedevice device-id",
        "handler": _delete_device,
        "argcount": 2
    },
    "querydevices": {
        "description": "List all devices with details",
        "syntax": "querydevices",
        "handler": _query_devices,
        "argcount": 1
    },
    "querydevice": {
        "description": "List a device by ID",
        "syntax": "querydevice device-id",
        "handler": _query_devices,
        "argcount": 2
    },
    "querydeviceprograms": {
        "description": "List all programs for a device ID",
        "syntax": "querydeviceprograms device-id",
        "handler": _query_device_programs,
        "argcount": 2
    },
    "querydeviceprogram": {
        "description": "List program details for a program ID",
        "syntax": "querydeviceprogram program-id",
        "handler": _query_device_program,
        "argcount": 2
    },
    "queryprograms": {
        "description": "List all programs for a device ID",
        "syntax": "queryprograms device-id",
        "handler": _query_device_programs,
        "argcount": 2
    },
    "queryprogram": {
        "description": "List program details for a program ID",
        "syntax": "queryprogram program-id",
        "handler": _query_device_program,
        "argcount": 2
    },
    "defineprogram": {
        "description": "Define a new program",
        "syntax": "defineprogram <new_device.json>",
        "handler": _define_program,
        "argcount": 2
    },
    "updateprogram": {
        "description": "Update a program",
        "syntax": "updateprogram <update_device.json>",
        "handler": _update_program,
        "argcount": 2
    },
    "deletedeviceprogram": {
        "description": "Delete a program by its program ID",
        "syntax": "deletedeviceprogram program-id",
        "handler": _delete_program,
        "argcount": 2
    },
    "deleteprogram": {
        "description": "Delete a program by its program ID",
        "syntax": "deleteprogram program-id",
        "handler": _delete_program,
        "argcount": 2
    },
}


def _get_request_handler(request_args):
    request = request_args[0].lower()
    if request in request_list.keys():
        if len(request_args) == request_list[request]["argcount"]:
            return request_list[request]
        else:
            print("Wrong number of request arguments")
            print(request_args)
            print("%d arguments required (including request), %d provided" % (request_list[request]["argcount"], len(request_args)))
    else:
        print("Unknown request:", args[0])

    return None


"""
AtHomePowerlineServer Client

python ahps_client.py [-s SERVER] [-p PORT] [-v | -q] request [request...argument(s)]

request
"""
if __name__ == "__main__":
    # Show license advertisement
    import disclaimer.Disclaimer

    disclaimer.Disclaimer.DisplayDisclaimer()

    # import pdb; pdb.set_trace()

    parser = OptionParser(usage="usage: %prog [options] request [arguments]")
    parser.add_option("-s", "--server", help="Server name or address")
    parser.add_option("-p", "--port", type="int", help="TCP port number for server")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=True, help="Verbose logging")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", help="Quiet/minimal logging")
    (options, args) = parser.parse_args()

    if options.server is not None:
        host = options.server
    if options.port is not None:
        port = int(options.port)
    verbose = options.verbose

    handler = _get_request_handler(args)
    if handler:
        handler["handler"](args)
