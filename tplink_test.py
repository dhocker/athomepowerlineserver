#
# TPLink smart plug device research
# Copyright © 2019  Dave Hocker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

from pyHS100 import SmartPlug, Discover


if __name__ == '__main__':
    # plug = SmartPlug("192.168.1.181")
    plug = Discover.discover_single("192.168.1.181")
    print("Plug:", plug.alias)
    print(plug)

    print()
    print("Hardware")
    print(plug.hw_info)

    print()
    print("Sys Info")
    print(plug.get_sysinfo())

    print()
    print("State:", plug.state)
