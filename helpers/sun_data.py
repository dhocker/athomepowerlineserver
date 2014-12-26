# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014, 2015  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from datetime import datetime
from astral import Astral
from Configuration import Configuration


def get_astral_data(for_datetime):
    '''
    Returns the sunrise and sunset times for the given date.
    Uses the Astral package to compute sunrise/sunset for the
    configured city.
    Reference https://pythonhosted.org/astral/module.html
    :param for_datetime:
    :return: Returns a dict containing the keys sunrise and sunset.
    The values are datetime objects.
    '''
    a = Astral()
    a.solar_depression = "civil"
    # We use a city just to get a city object. Then we override the lat/long.
    # The city object can produce sunrise/sunset in local time.
    if Configuration.City() != "":
        city = a[Configuration.City()]
    else:
        # Default if no city is configured
        city = a["New York"]
    if Configuration.Latitude() != "":
        city.latitude = float(Configuration.Latitude())
    if Configuration.Longitude() != "":
        city.longitude = float(Configuration.Longitude())

    return city.sun(date=for_datetime, local=True)


def get_sun_data(for_datetime):
    '''
    Returns the sunrise and sunset times for the given date.
    Uses the Astral package to compute sunrise/sunset for the
    configured city.
    Reference https://pythonhosted.org/astral/module.html
    :param for_datetime:
    :return: Returns a dict containing the keys sunrise and sunset.
    '''

    sun_data = get_astral_data(for_datetime)

    sun_data_response = {}
    sun_data_response["sunrise"] = sun_data["sunrise"].isoformat()
    sun_data_response["sunset"] = sun_data["sunset"].isoformat()

    return sun_data_response


def round_to_minute(time_to_round):
    round_adj = 0
    if time_to_round.second >= 30:
        round_adj = 1
    rounded = datetime(time_to_round.year, time_to_round.month, time_to_round.day,
                       hour=time_to_round.hour, minute=(time_to_round.minute + round_adj), second=0, microsecond=0,
                       tzinfo=time_to_round.tzinfo)
    return rounded


def get_sunrise(for_datetime):
    """
    Return the sunrise time for a given date/time
    """

    sun_data = get_astral_data(for_datetime)

    # Returns a datetime instance in local time
    return round_to_minute(sun_data["sunrise"])


def get_sunset(for_datetime):
    """
    Return the sunset time for a given date/time
    """

    sun_data = get_astral_data(for_datetime)

    # Returns a datetime instance in local time
    return round_to_minute(sun_data["sunset"])
