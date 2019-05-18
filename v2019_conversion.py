#
# AtHomePowerlineServer - database conversion for v2019
# Copyright © 2019  Dave Hocker (email: AtHomeX10@gmail.com)
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


def delete_devices(conn):
    c = get_cursor(conn)
    c.execute("DELETE FROM Devices")
    conn.commit()


def insert_device(conn, device_name, device_type, device_address):
    """
    Insert a new device record
    :param device_name: name/tag/label for the device (human readable)
    :param device_type: device type (e.g. x10, tplink, hs100, etc.)
    :param device_address: x10 house-device-code or ip address or ...
    :return:
    """
    if device_type not in ["x10"]:
        return -1

    c = get_cursor(conn)
    # SQL insertion safe...
    # Note that the current time is inserted as the update time. This is added to the
    # row as a convenient way to know when the record was inserted. It isn't used for
    # any other purpose.
    c.execute("INSERT INTO Devices (name,location,type,address, selected,updatetime) values (?,?,?,?,?,?)",
              (device_name, "", device_type, device_address, False, datetime.datetime.now()))
    id = c.lastrowid
    conn.commit()
    return id

def get_device_record_for_hdc(conn, hdc):
    c = get_cursor(conn)
    rset = c.execute("SELECT * from Devices where address=?", (hdc,))
    if rset:
        return rset.fetchall()
    return None


def get_action_record(conn, name):
    c = get_cursor(conn)
    rset = c.execute("SELECT * from Actions where name=?", (name,))
    if rset:
        return rset.fetchone()
    return None


def get_all_timers(conn):
    c = get_cursor(conn)
    rset = c.execute("SELECT * from Timers")
    return rset


def update_timer(conn, name, device_id):
    c = get_cursor(conn)
    c.execute("UPDATE Timers SET deviceid=? where name=?", (device_id, name, ))
    conn.commit()


def get_column_names(conn, table_name):
    c = get_cursor(conn)
    # c.execute("SELECT * from sqlite_master where name=?", (table_name, ))
    # Unfortunatel SQLite does not seem to support substitution
    sql = "pragma table_info(%s)" % table_name
    c.execute(sql)
    rset = c.fetchall()
    col_names = []
    for col in rset:
        col_names.append(col["name"])
    return col_names


def get_table_names(conn):
    c = get_cursor(conn)
    rset = c.execute("SELECT name from sqlite_master")
    tables = []
    for r in rset:
        tables.append(r["name"])
    return tables


def update_devices_table(conn):
    tables = get_table_names(conn)
    if "Devices" not in tables:
        conn.execute(
            "CREATE TABLE Devices (id integer PRIMARY KEY, name text, location text, \
            type text, address text, selected integer, updatetime timestamp)")
        conn.commit()
        print("Devices table created")
    else:
        print("Devices table already exists")
        device_cols = get_column_names(conn, "Devices")
        if "location" not in device_cols:
            print("Adding location column to Devices table")
            c = get_cursor(conn)
            c.execute("ALTER TABLE Devices ADD COLUMN location TEXT")
            conn.commit()
        if "selected" not in device_cols:
            print("Adding selected column to Devices table")
            c = get_cursor(conn)
            c.execute("ALTER TABLE Devices ADD COLUMN selected INTEGER")
            conn.commit()


def update_schema_first():
    """
    Because SQLite3 does not support deleting columns,
    the schema must be updated in two passes. The first
    pass adds new columns and tables. The second pass will
    remove columns.
    :return: None
    """
    conn = get_connection()

    # Create Devices table if necessary
    update_devices_table(conn)

    # Create temp table for split of Timers table

    # Each record is a single timer/action pair
    conn.execute("CREATE TABLE temptimers (id integer PRIMARY KEY, \
                 name text, deviceid integer, daymask text, \
                 triggermethod text, time timestamp, offset integer, \
                 randomize integer, randomizeamount integer, \
                 command text, dimamount integer, args text, updatetime timestamp, \
                 FOREIGN KEY(deviceid) REFERENCES Devices(id))")

    # Update schema version record
    c = get_cursor(conn)
    c.execute("DELETE FROM SchemaVersion")
    c.execute("INSERT INTO SchemaVersion values (?,?)", ("4.0.0.0", datetime.datetime.now(), ))
    conn.commit()
    print("SchemaVersion updated")

    conn.close()


def update_schema_last():
    """
    This is the second pass of the schema update.
    :return:
    """
    conn = get_connection()

    # Delete Actions table. No longer needed.
    conn.execute("DROP TABLE IF EXISTS Actions")

    conn.close()


def create_devices():
    print("Creating devices used by Timers")

    conn = get_connection()

    # Clean house
    delete_devices(conn)

    # Define all devices used by timers
    timers = get_all_timers(conn)
    for t in timers:
        hdc = t["housedevicecode"].upper()
        print(hdc)
        # Skip house codes
        if len(hdc) == 1:
            print("Skipping house code %s" % hdc)
            continue
        # Check to see if this hdc is already defined
        r = get_device_record_for_hdc(conn, hdc)
        if r and len(r) >= 1:
            print("Device %s is already defined" % hdc)
            continue
        device_name = "X10-" + hdc
        insert_device(conn, device_name, "x10", hdc)
        print("Device %s defined" % hdc)

    conn.close()


def insert_temptimers_record(conn, name, deviceid, daymask, triggermethod, time, offset,
                             randomize, randomizeamount, command, dimamount, args):
    c = get_cursor(conn)
    c.execute("INSERT INTO temptimers (name, deviceid, daymask, triggermethod, time, offset, \
              randomize, randomizeamount, command, dimamount, args, updatetime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (name, deviceid, daymask, triggermethod, time, offset,
              randomize, randomizeamount, command, dimamount, args,
              datetime.datetime.now()))
    conn.commit()


def split_timers_record(conn, rec):
    name = rec["name"]
    hdc = rec["housedevicecode"].upper()
    print("Splitting Timers record %s" % name)

    # Skip house codes
    if len(hdc) == 1:
        print("Skipping house code %s for timer" % hdc, name)
        return

    # Find the device record. Only one record should be returned.
    r = get_device_record_for_hdc(conn, hdc)
    if r and len(r) >= 1:
        deviceid = r[0]["id"]
    else:
        print("No device record found for %s" % hdc)
        return

    # Get start and stop action records
    start_rec = get_action_record(conn, rec["startaction"])
    stop_rec = get_action_record(conn, rec["stopaction"])

    # Insert temptimer records, one for start and one for stop
    # After this, the Actions table is no longer needed
    insert_temptimers_record(conn, "start " + name, deviceid, rec["daymask"], rec["starttriggermethod"],
                             rec["starttime"], rec["startoffset"], rec["startrandomize"],
                             rec["startrandomizeamount"], start_rec["command"],
                             start_rec["dimamount"], start_rec["args"])
    insert_temptimers_record(conn, "stop " + name, deviceid, rec["daymask"], rec["stoptriggermethod"],
                             rec["stoptime"], rec["stopoffset"], rec["stoprandomize"],
                             rec["stoprandomizeamount"], stop_rec["command"],
                             stop_rec["dimamount"], stop_rec["args"])


def update_timers():
    # Split each record of old Timers table into 2 records in the temp Timers table
    print("Splitting Timers table into start and stop records using device IDs")

    conn = get_connection()

    # Split each existing timer record into 2 new temp timer records
    timers = get_all_timers(conn)
    for t in timers:
        split_timers_record(conn, t)

    # Delete existing Timers table and rename temptimers table
    conn.execute("DROP TABLE IF EXISTS Timers")
    conn.execute("ALTER TABLE temptimers RENAME TO Timers")
    conn.commit()

    conn.close()


def main():
    schema_version = get_schema_version()
    if schema_version != "4.0.0.0":
        update_schema_first()
        create_devices()
        update_timers()
        update_schema_last()
    else:
        print("Database already up to date")


if __name__ == "__main__":
    import sys
    testing = len(sys.argv) > 1 and sys.argv[1].lower() == "testing"
    if testing:
        # For testing
        db = "x.sqlite3"
    else:
        # For production, get database path from configuration
        from Configuration import Configuration
        Configuration.LoadConfiguration()
        db = Configuration.GetDatabaseFilePath("AtHomePowerlineServer.sqlite3")
    print("Converting %s to v2019" % db)
    main()
