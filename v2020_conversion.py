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


def update_schema_version():
    """
    :return: None
    """
    conn = get_connection()

    # Update schema version record
    c = get_cursor(conn)
    c.execute("DELETE FROM SchemaVersion")
    c.execute("INSERT INTO SchemaVersion values (?,?)", ("5.0.0.0", datetime.datetime.now(), ))
    conn.commit()
    print("SchemaVersion updated")

    conn.close()


def update_devices():
    """
    Go through the hoops of renaming the Devices.type column
    :return:
    """
    conn = get_connection()

    # Rename type column to mfg
    c = get_cursor(conn)

    # Temp table
    conn.execute(
        "CREATE TABLE DevicesTemp (id integer PRIMARY KEY, name text, location text, \
        mfg text, address text, selected integer, updatetime timestamp)")
    # Copy all rows from Devices
    conn.execute(
        "INSERT INTO DevicesTemp(id,name,location,mfg,address,selected,updatetime) \
        SELECT id,name,location,type,address,selected,updatetime from Devices")
    # Delete Devices table
    conn.execute("DROP TABLE Devices")
    # Rename temp table to ManagedDevices
    conn.execute("ALTER TABLE DevicesTemp RENAME TO ManagedDevices")

    # c.execute("DELETE FROM SchemaVersion")
    # c.execute("INSERT INTO SchemaVersion values (?,?)", ("5.0.0.0", datetime.datetime.now(), ))

    conn.commit()
    print("Devices updated")

    conn.close()


def rename_timers():
    conn = get_connection()

    conn.execute("ALTER TABLE Timers RENAME TO Programs")

    conn.commit()
    print("Timers renamed to Programs")

    conn.close()


def create_program_assignments():
    conn = get_connection()

    conn.execute(
        "CREATE TABLE ProgramAssignments (id integer PRIMARY KEY, \
        device_id integer NOT NULL, program_id integer NOT NULL, \
        FOREIGN KEY (device_id) REFERENCES ManagedDevices(id) ON DELETE CASCADE, \
        FOREIGN KEY (program_id) REFERENCES Programs(id) ON DELETE CASCADE, \
        UNIQUE (device_id, program_id))"
    )

    # Each row of the Programs table produces a program assignment record
    conn.execute(
        "INSERT INTO ProgramAssignments(device_id,program_id) \
        SELECT deviceid,id from ProgramsTemp")

    # This is a bit crazy, but Sqlite seems to get confused when
    # tables are renamed. To delete the deviceid column out of the
    # old Devices table, we had to rename it and make a copy without
    # the column. Now that we are done with the copy, we can delete it.
    conn.execute("DROP TABLE ProgramsTemp")

    conn.commit()
    print("ProgramAssignments created")

    conn.close()


def delete_programs_deviceid_column():
    """
    :return:
    """
    conn = get_connection()

    conn.execute("ALTER TABLE Programs RENAME TO ProgramsTemp")
    conn.commit()

    # New Programs table without device ID column
    conn.execute(
        "CREATE TABLE Programs ( \
        id	integer, \
        name	text, \
        daymask	text, \
        triggermethod	text, \
        time	timestamp, \
        offset	integer, \
        randomize	integer, \
        randomizeamount	integer, \
        command	text, \
        dimamount	integer, \
        args	text, \
        updatetime	timestamp, \
        PRIMARY KEY(id) ) \
        "
    )
    conn.commit()

    # Copy the temp table, losing the device ID in the process.
    conn.execute(
        "INSERT INTO Programs(id,name,daymask,triggermethod,time,offset,randomize,randomizeamount,command,dimamount,args,updatetime) \
        SELECT id,name,daymask,triggermethod,time,offset,randomize,randomizeamount,command,dimamount,args,updatetime from ProgramsTemp")
    conn.commit()

    conn.commit()
    print("Programs.deviceid dropped")

    conn.close()


def create_group_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # ActionGroups table
    conn.execute(
        "CREATE TABLE ActionGroups (id integer PRIMARY KEY, name text)"
    )

    # ActionGroupDevices table
    cursor.execute(
        "CREATE TABLE ActionGroupDevices (id integer PRIMARY KEY, group_id integer , device_id integer, \
        FOREIGN KEY (device_id) REFERENCES ManagedDevices(id) ON DELETE CASCADE, \
        FOREIGN KEY (group_id) REFERENCES ActionGroups(id) ON DELETE CASCADE, \
        UNIQUE(group_id,device_id))"
    )

    # Populate groups table with unique location names in the new ManagedDevices tables
    cursor.execute(
        "INSERT INTO ActionGroups (name) \
        SELECT DISTINCT location FROM ManagedDevices"
    )
    # Automatically create a group for Selected devices
    cursor.execute(
        'INSERT INTO ActionGroups (name) VALUES ("Selected")'
    )
    selected_id = cursor.lastrowid
    # Add all managed devices that are "selected" to the ActionGroupDevices
    cursor.execute(
        "INSERT INTO ActionGroupDevices (group_id,device_id) \
        SELECT %d,id FROM ManagedDevices WHERE selected=1" % selected_id
    )

    conn.commit()
    print("Group tables created")

    conn.close()


def drop_selected_column():
    """
    Drop the selected column from the ManagedDevices table.
    This has to be done AFTER the ActionGroupTable is created
    as it depends on the old selected column to assign devices
    to the new "Selected" group.
    :return:
    """
    conn = get_connection()

    # Temp table without "selected" column
    conn.execute(
        "CREATE TABLE ManagedDevicesTemp (id integer PRIMARY KEY, name text, location text, \
        mfg text, address text, updatetime timestamp)")
    # Copy all rows from ManagedDevices
    conn.execute(
        "INSERT INTO ManagedDevicesTemp(id,name,location,mfg,address,updatetime) \
        SELECT id,name,location,mfg,address,updatetime from ManagedDevices")
    # Delete ManagedDevices table
    conn.execute("DROP TABLE ManagedDevices")
    # Rename temp table to ManagedDevices
    conn.execute("ALTER TABLE ManagedDevicesTemp RENAME TO ManagedDevices")

    conn.commit()
    print("Selected column dropped from ManageDevices table")

    conn.close()


def delete_sun_table():
    # Clean up dead table
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS sun_table")
    conn.commit()
    print("sun_table dropped")
    conn.close()


def main():
    v2020_schema = "5.0.0.0"
    schema_version = get_schema_version()
    if schema_version == "4.0.0.0":
        # Rename Timers to Programs
        rename_timers()
        # Delete no longer needed column
        delete_programs_deviceid_column()
        # Create program assignments from Programs table before deleting device ID column
        create_program_assignments()
        # Rename Devices.type to Devices.mfg
        update_devices()
        # Create ActionGroup related tables
        create_group_tables()
        # Drop "selected" column from ManagedDevices
        drop_selected_column()
        # Clean up unused table
        delete_sun_table()
        # To 5.0.0.0
        update_schema_version()
    elif schema_version == v2020_schema:
        print("Database is already at version %s" % v2020_schema)
    else:
        print("Conversion from %s to %s is not supported" % schema_version, v2020_schema)


if __name__ == "__main__":
    import sys
    print("AtHomePowerlineServer Database conversion from version 4.0.0.0 to 5.0.0.0")
    testing = len(sys.argv) > 1 and sys.argv[1].lower() == "testing"
    if testing:
        # For testing
        db = "x.sqlite3"
    else:
        # For production, get database path from configuration
        from Configuration import Configuration
        Configuration.LoadConfiguration()
        db = Configuration.GetDatabaseFilePath("AtHomePowerlineServer.sqlite3")
    print("Converting %s to 5.0.0.0" % db)
    main()
