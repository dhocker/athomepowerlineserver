#
# Kasa/TPLink device driver for TPLink/Kasa devices
# Based on python-kasa package: https://github.com/python-kasa/python-kasa
# © 2020, 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from Configuration import Configuration
from .base_thread_driver import BaseThreadDriver
from .pykasa_adapter_thread import PyKasaAdapterThread
import logging

logger = logging.getLogger("server")


class PyKasaDriver(BaseThreadDriver):
    """
    Driver for TPLink/Kasa devices (SmartPlugs, SmartSwitch, SmartStrip, SmartBulb).
    Uses python-kasa package. The whole purpose of this class is to
    relay requests to the thread where the actual driver is running.
    """

    def __init__(self):
        """
        Initialize an instance of the python-kasa based driver
        """
        super().__init__(adapter_thread=PyKasaAdapterThread())
        self._loop = None
        self._all_devices = None
        logger.info("PyKasa driver initialized")

    def open(self, kwargs=None):
        """
        Queue an open request
        :param kwargs: None expected
        :return:
        """
        kwargs = {
            "discover_target": Configuration.PyKasaDiscoverTarget()
        }

        # Run the request on the adapter thread
        result = super().open(kwargs=kwargs)

        return result
