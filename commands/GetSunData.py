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

#
# GetTime
#

import commands.ServerCommand as ServerCommand
import datetime
from helpers.sun_data import get_sunrise, get_sunset

#######################################################################
# Command handler for GetSunData command
class GetSunData(ServerCommand.ServerCommand):
  
  #######################################################################
  # Execute the GetTime command.
  def Execute(self, request):     
    # Generate a response
    response = GetSunData.CreateResponse("GetSunData")
    r = response["X10Response"]
    r['data'] = {}

    # Date should be in ISO format: YYYY-MM-DD
    for_date_str = request["args"]["date"]
    for_datetime = datetime.datetime.strptime(for_date_str, "%Y-%m-%d")

    # The sun_data functions expect a date type, so we convert to date here
    for_date = datetime.date(for_datetime.year, for_datetime.month, for_datetime.day)

    sunset_dt = get_sunset(for_date)
    sunrise_dt = get_sunrise(for_date)

    r['data']['sunset'] = sunset_dt.isoformat()
    r['data']['sunrise'] = sunrise_dt.isoformat()

    # Success
    r['result-code'] = 0
    r['message'] = "Success"

    return response