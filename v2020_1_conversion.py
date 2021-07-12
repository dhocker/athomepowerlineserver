#
# AtHomePowerlineServer - database conversion from v2019 to v2020
# Copyright © 2020  Dave Hocker (email: AtHomeX10@gmail.com)
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

import sqlite3
import datetime

# This is the database being converted
db = ""


def get_connection():
    conn = sqlite3.connect(db)
    # We use the row factory to get named row columns. Makes handling row sets easier.
    conn.row_factory = sqlite3.Row
    # The default string type is unicode. This changes it to UTF-8.
    conn.text_factory = str
    return conn


def get_cursor(conn):
    return conn.cursor()


def get_schema_version():
    conn = get_connection()
    c = get_cursor(conn)
    rset = c.execute("SELECT * FROM SchemaVersion")
    r = rset.fetchone()
    version = r["Version"]
    conn.close()
    return version


def update_schema_version(to_schema_version):
    """
    :return: None
    """
    conn = get_connection()

    # Update schema version record
    c = get_cursor(conn)
    c.execute("DELETE FROM SchemaVersion")
    c.execute("INSERT INTO SchemaVersion values (?,?)", (to_schema_version, datetime.datetime.now(), ))
    conn.commit()
    print("SchemaVersion updated")

    conn.close()


def update_managed_devices():
    """
    Go through the hoops of adding ManagedDevices.channel column
    :return: None
    """
    conn = get_connection()

    # Temp table with new channel column
    conn.execute(
        "CREATE TABLE DevicesTemp (id integer PRIMARY KEY, name text, location text, \
        mfg text, address text, channel integer, updatetime timestamp)")
    # Copy all rows from ManagedDevices. Default channel to 0.
    conn.execute(
        "INSERT INTO DevicesTemp(id,name,location,mfg,address,channel,updatetime) \
        SELECT id,name,location,mfg,address,0,updatetime from ManagedDevices")
    # Delete ManagedDevices table
    conn.execute("DROP TABLE ManagedDevices")
    # Rename temp table to ManagedDevices
    conn.execute("ALTER TABLE DevicesTemp RENAME TO ManagedDevices")

    conn.commit()
    print("ManagedDevices updated")

    conn.close()


def main():
    next_schema_version = "5.1.0.0"
    current_schema_version = get_schema_version()
    if current_schema_version == "5.0.0.0":
        # Add channel column to ManagedDevices
        update_managed_devices()
        # To 5.1.0.0
        update_schema_version(next_schema_version)
    elif current_schema_version == next_schema_version:
        print("Database is already at version %s" % next_schema_version)
    else:
        print("Conversion from %s to %s is not supported" % current_schema_version, next_schema_version)


if __name__ == "__main__":
    import sys
    print("AtHomePowerlineServer Database conversion from version 5.0.0.0 to 5.1.0.0")
    testing = len(sys.argv) > 1 and sys.argv[1].lower() == "testing"
    if testing:
        # For testing
        db = "x.sqlite3"
    else:
        # For production, get database path from configuration
        from Configuration import Configuration
        Configuration.load_configuration()
        db = Configuration.GetDatabaseFilePath("AtHomePowerlineServer.sqlite3")
    print("Converting %s to 5.1.0.0" % db)
    main()
