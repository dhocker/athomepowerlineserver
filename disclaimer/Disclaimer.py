# -*- coding: utf-8 -*-#
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

#######################################################################

import logging
import Version

logger = logging.getLogger("server")

_disclaimer = [
    "",
    "AtHomePowerlineServer Copyright © 2014, 2020 Dave Hocker (AtHomeX10@gmail.com)",
    "Version {0}".format(Version.GetVersion()),
    "",
    "This program comes with ABSOLUTELY NO WARRANTY; for details see the LICENSE file.",
    "This is free software, and you are welcome to redistribute it",
    "under certain conditions; see the LICENSE file for details.",
    ""
]


def DisplayDisclaimer():
    """
    Show the disclaimer as recommended by the GPL v3 license
    """
    for line in _disclaimer:
        print(line)


def LogDisclaimer():
    """
    Show the disclaimer as recommended by the GPL v3 license
    """
    for line in _disclaimer:
        logger.info(line)
