#
# internet_utils
# Copyright © 2022  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

import time
import logging
import ntplib


logger = logging.getLogger("server")


def is_internet_up(ntp_server="time.nist.gov", max_time=0.0, wait_time=5.0):
    """
    Verify Internet access. This is required for Meross devices to work.
    This is mostly about recovering from power outages.
    :param ntp_server: An NTP server to contact.
    :param max_time: Maximum amount of time to consume. A value of 0.0 means "forever".
    :param wait_time: How long to wait between connection attempts
    :return: Returns True if internet is accessible
    """
    logger.info("Verifying Internet connection...")
    ntp_client = ntplib.NTPClient()
    elapsed_time = 0.0
    while max_time == 0.0 or elapsed_time < max_time:
        try:
            # Internet access is verified by connecting to a reliable, well-known
            # server (in this case an NTP server).
            response = ntp_client.request(ntp_server)
            if response is not None:
                logger.info("Internet verification successful")
                return True
            time.sleep(wait_time)
            elapsed_time += wait_time
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt terminated Internet check")
            break
        except ntplib.NTPException:
            # Wait and try again
            time.sleep(wait_time)
            elapsed_time += wait_time
        except Exception as e:
            logger.error("Unhandled exception occurred during Internet verification")
            logger.error(str(e))
            # logger.error(sys.exc_info()[0])
            time.sleep(wait_time)
            elapsed_time += wait_time

    # Internet test failed
    logger.error("Internet check failed")
    return False
