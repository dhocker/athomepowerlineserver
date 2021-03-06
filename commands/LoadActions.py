# -*- coding: utf-8 -*-
#
# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright © 2014, 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import commands.ServerCommand as ServerCommand
import database.Actions
import logging

logger = logging.getLogger("server")


#######################################################################
# TODO Remove
# Command handler for loading actions used by timer programs
class LoadActions(ServerCommand.ServerCommand):

    #######################################################################
    # Execute the load actions command.
    # We replace the current set of timer programs/initiators with
    # whatever is in the request payload.
    def Execute(self, request):
        # Reset the actions list to empty
        database.Actions.Actions.DeleteAll()

        # Generate a starting response
        r = LoadActions.CreateResponse("LoadAction")

        for action in request["args"]["actions"]:
            # Pull all of the timer program values out of the dict entry
            name = action["name"]
            command = action["command"]
            dim_amount = action["dim-amount"]

            try:
                # Add the action to the current list
                database.Actions.Actions.Insert(name, command, dim_amount, "")
            except Exception as ex:
                logger.error(str(ex))
                r['result-code'] = 1
                r['error'] = "Actions insert failed. Is the name unique?"
                r['message'] = "Failure"
                return r

        # Debugging...
        database.Actions.Actions.DumpActions()

        # Success
        r['result-code'] = 0
        # r['error'] = "Command not implemented"
        r['message'] = "Success"

        return r
