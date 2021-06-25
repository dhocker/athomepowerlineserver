#
# Meross async i/o based driver
# Copyright © 2021  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#
# This driver works with the meross-iot module at version 0.4+.
#

from .base_thread_driver import BaseThreadDriver
from .meross_adapter_thread import MerossAdapterThread
from Configuration import Configuration
import logging

logger = logging.getLogger("server")


class MerossDriverV4(BaseThreadDriver):
    """
    Meross device driver. Most of the methods are in the base class.
    """
    MEROSS_ERROR = 7
    RETRY_COUNT = 5

    def __init__(self, request_wait_time=60.0):
        logger.info("Meross adapter thread initialization started")

        # The base class does most of the work
        super().__init__(adapter_thread=MerossAdapterThread(), request_wait_time=request_wait_time)

        logger.info("MerossDriverV4 initialized")

    def open(self, kwargs=None):
        """
        Queue an open request
        :param kwargs: None expected
        :return:
        """
        kwargs = {
            "email": Configuration.MerossEmail(),
            "password": Configuration.MerossPassword()
        }

        # Run the request on the adapter thread
        result = super().open(kwargs=kwargs)

        return result
