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
    c.execute("INSERT INTO Devices (name,type,address,updatetime) values (?,?,?,?)",
              (device_name, device_type, device_address, datetime.datetime.now()))
    id = c.lastrowid
    conn.commit()
    return id

def get_device_record_for_hdc(conn, hdc):
    c = get_cursor(conn)
    rset = c.execute("SELECT * from Devices where address=?", (hdc,))
    if rset:
        return rset.fetchall()
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


def update_schema():
    conn = get_connection()
    c = get_cursor(conn)
    rset = c.execute("SELECT * FROM SchemaVersion")
    r = rset.fetchone()

    if r["Version"] != "4.0.0.0":
        # If Timers does not have a deviceid column, add it
        timer_cols = get_column_names(conn, "Timers")
        if "deviceid" not in timer_cols:
            print("Adding deviceid column to Timers table")
            c = get_cursor(conn)
            c.execute("ALTER TABLE Timers ADD COLUMN deviceid INTEGER")
            conn.commit()
        else:
            print("deviceid column already in Timers table")

        # Create Devices table
        conn.execute(
            "CREATE TABLE Devices (id integer PRIMARY KEY, name text, type text, address text, updatetime timestamp)")
        conn.commit()
        print("Devices table created")

        # Update schema version record
        c = get_cursor(conn)
        c.execute("DELETE FROM SchemaVersion")
        c.execute("INSERT INTO SchemaVersion values (?,?)", ("4.0.0.0", datetime.datetime.now(), ))
        conn.commit()
        print("SchemaVersion updated")

    else:
        print("Schema is up to date")

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


def update_timers():
    print("Updating Timers to use assigned device IDs")

    conn = get_connection()

    # Set device ID for each timer
    timers = get_all_timers(conn)
    for t in timers:
        name = t["name"]
        hdc = t["housedevicecode"].upper()
        print(name)

        # Skip house codes
        if len(hdc) == 1:
            print("Skipping house code %s" % hdc)
            continue

        # Find the device record. ONly one record should be returned.
        r = get_device_record_for_hdc(conn, hdc)
        if r and len(r) >= 1:
            print("Updating Timer record %s" % name)
            update_timer(conn, name, r[0]["id"])
        else:
            print("No device record found for %s" % hdc)

    conn.close()


def main():
    update_schema()
    create_devices()
    update_timers()

if __name__ == "__main__":
    db = "x.sqlite3"
    # TODO Create Devices table as needed
    # TODO Add deviceid column to Timers as needed
    print("Converting %s to v2019" % db)
    main()
    # conn = get_connection()
    # col_names = get_column_names(conn, "Timers")
    # for col in col_names:
    #     print("Column name: %s" % col)
