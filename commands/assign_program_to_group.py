#
# Assign a program to a group's devices
# Copyright © 2020  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from commands.ServerCommand import ServerCommand
from database.program_assignments import ProgramAssignments
from database.action_group_devices import ActionGroupDevices


class AssignProgramToGroup(ServerCommand):
    """
    Command handler for assigning a program to a device
    """
    def Execute(self, request):
        group_id = int(request["args"]["group-id"])
        program_id = int(request["args"]["program-id"])

        r = self.CreateResponse(request["request"])

        # Devices in group
        agd = ActionGroupDevices()
        devices = agd.get_group_devices(group_id)
        if devices is None:
            r['result-code'] = agd.last_error_code
            r['message'] = agd.last_error
            return r

        # For each device in the group...
        assigned_count = 0
        already_assigned_count = 0
        for device in devices:
            # Is the program already assigned to this device?
            # We DO NOT depend on the invoker to only add programs once
            assigned = ProgramAssignments.is_assigned(device["id"], program_id)
            # If it isn't, assign the program
            if not assigned:
                ProgramAssignments.insert(device["id"], program_id)
                assigned_count += 1
            else:
                already_assigned_count += 1

        # Generate a successful response
        r['result-code'] = ServerCommand.SUCCESS
        r['group-id'] = group_id
        r['program-id'] = program_id
        r['assigned-count'] = assigned_count
        r['already-assigned-count'] = already_assigned_count
        r['message'] = ServerCommand.MSG_SUCCESS

        return r
