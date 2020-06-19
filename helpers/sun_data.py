# AtHomePowerlineServer - networked server for CM11/CM11A/XTB-232 X10 controllers
# Copyright (C) 2014, 2015  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
from astral.geocoder import database, lookup
from Configuration import Configuration


def get_astral_data(for_datetime):
    '''
    Returns the sunrise and sunset times for the given date.
    Uses the Astral package to compute sunrise/sunset for the
    configured city.
    Reference https://astral.readthedocs.io/en/latest/index.html
    :param for_datetime: The date for the astral data
    :return: Returns a dict containing the keys sunrise and sunset.
    The values are datetime objects.
    '''
    city = None
    # Either city/name or latitude and longitude are required
    if Configuration.City() != "":
        db = database()
        try:
            city = lookup(Configuration.City(), db)
            # Overrides
            if Configuration.Latitude() != "":
                city.latitude = float(Configuration.Latitude())
            if Configuration.Longitude() != "":
                city.longitude = float(Configuration.Longitude())
        except KeyError:
            pass

    if city is None:
        # Default if no city is configured
        city = LocationInfo()
        # We expect latitude and longitude to be configured to override city
        if Configuration.Latitude() != "" and Configuration.Longitude() != "":
            city.latitude = float(Configuration.Latitude())
            city.longitude = float(Configuration.Longitude())
        else:
            raise ValueError("Latitude and longitude are required")

    # region is not used
    # city.region = ""

    # Local timezone
    city.timezone = datetime.now().astimezone().tzinfo

    return sun(city.observer, date=for_datetime, tzinfo=city.timezone)


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
    rounded = datetime(time_to_round.year, time_to_round.month, time_to_round.day,
                       hour=time_to_round.hour, minute=time_to_round.minute, second=0, microsecond=0,
                       tzinfo=time_to_round.tzinfo)
    if time_to_round.second >= 30:
        round_adj = timedelta(minutes=1)
        rounded = rounded + round_adj
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
