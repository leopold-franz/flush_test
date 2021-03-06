# To install psycopg2
# 1. sudo apt-get install libpq-dev
# 2. pip install psycopg2
import psycopg2
from psycopg2 import sql
from datetime import datetime


def connect_database(user, password, host, port, db_name, verbose=False):
    """
    Connects to database on host and port given as user using password to authenticate user. Return connection cursor.

    Args:
        user: str User of database
        password: str Password of user
        host: str IP of host
        port: int Port to connect to database on host
        db_name: str Database name
        verbose: bool Boolean to add additional information to log. Default False

    Returns:
        connection Database connection object (If not None needs to be closed)
        cursor Cursor of connection to database
    """
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=db_name)

    cursor = connection.cursor()
    if verbose:
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
    return connection, cursor


def close_database_connection(connection, cursor):
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


def add_user(sql_cursor, first_name, last_name, dob):
    """
    Add a user to the users table of database the sql cursor is connected to.

    Args:
        sql_cursor: sql connection cursor from psycopg2
        first_name: str First name of user
        last_name: str Last name of user
        dob: date Date of Birth of user

    Returns:
        user_id: int Identification token of toilet
    """

    sql_cmd = sql.SQL("""
        INSERT INTO users (first_name, last_name, date_of_birth)
        VALUES({first_name}, {last_name}, {dob})
        RETURNING user_id;
    """).format(first_name=sql.Literal(first_name),
                last_name=sql.Literal(last_name),
                dob=sql.Literal(str(dob)))
    sql_cursor.execute(sql_cmd)
    record = sql_cursor.fetchone()
    if not record:  # Check that a proper result value is given back
        return False
    # print("Result:", record, "\n")
    return record[0]


def add_toilet(sql_cursor, toilet_type, address, location, status):
    """
    Add a toilet to the toilets table of database the sql cursor is connected to.

    Args:
        sql_cursor: sql connection cursor from psycopg2
        toilet_type: str(max. 10 characters) Type of toilet
        address: str Address of toilet
        location: str Room or descriptive location of toilet in building
        status: str(max. 10 characters) Status of toilet (Active, Broken, Decommision)

    Returns:
        toilet_id: int Identification token of toilet
    """

    sql_cmd = sql.SQL("""
        INSERT INTO toilets (type, address, location, status)
        VALUES({ttype}, {addr}, {loc}, {status})
        RETURNING toilet_id;
    """).format(ttype=sql.Literal(toilet_type),
                addr=sql.Literal(address),
                loc=sql.Literal(location),
                status=sql.Literal(status))
    sql_cursor.execute(sql_cmd)
    record = sql_cursor.fetchone()
    if not record:  # Check that a proper result value is given back
        return False
    # print("Result:", record, "\n")
    return record[0]


def add_event(sql_cursor, user_id, toilet_id, timestamp_start, timestamp_end, status):
    """
    Add an event entry to the events table of database the sql cursor is connected to.

    Args:
        sql_cursor: sql connection cursor from psycopg2
        user_id: int Identification token of toilet
        toilet_id: int Identification token of toilet
        timestamp_start: timestamp with timezone Time of first measurement (When the user first sits down)
        timestamp_end: timestamp with timezone Time of last measurement (When the user stands up)
        status: str(max. 10 char long) Event status

    Returns:
        event_id: int Identification token of generated event
    """

    sql_cmd = sql.SQL("""
        INSERT INTO events (user_id, toilet_id, timestamp_start, timestamp_end, status)
        VALUES({uid}, {tid}, {ts_start}, {ts_end}, {status})
        RETURNING event_id;
    """).format(uid=sql.Literal(user_id),
                tid=sql.Literal(toilet_id),
                ts_start=sql.Literal(timestamp_start),
                ts_end=sql.Literal(timestamp_end),
                status=sql.Literal(status))
    sql_cursor.execute(sql_cmd)
    record = sql_cursor.fetchone()
    if not record:  # Check that a proper result value is given back
        return False
    # print("Event Result:", record, "\n")
    return record[0]


def add_raw_measurement(sql_cursor, event_id, timestamp, temperature, humidity, pressure, weight_seat, weight_floor,
                        gas_co2, gas_ch4, gas_nox, gas_cox, gas_voc, gas_nh3, tof_1, tof_2, tof_3, tof_4):
    """
    Add an event entry to the events table of database the sql cursor is connected to.

    Args:
        sql_cursor: sql connection cursor from psycopg2
        event_id: int Identification token of event
        timestamp: timestamp with timezone Time of measurement
        temperature: double Temperature
        humidity: double Humidity
        pressure: double Pressure
        weight_seat: double Weight measured from seat sensors
        weight_floor: double Weight measured from weight sensors
        gas_co2: double Gas measurement of CO2
        gas_ch4: double Gas measurement of CH4
        gas_nox: double Gas measurement of NOX
        gas_cox: double Gas measurement of COX
        gas_voc: double Gas measurement of VOC
        gas_nh3: double Gas measurement of NH3
        tof_1: double Time of Flight measurement of sensor 1
        tof_2: double Time of Flight measurement of sensor 2
        tof_3: double Time of Flight measurement of sensor 3
        tof_4: double Time of Flight measurement of sensor 4

    Returns:
        None
    """
    sql_cmd = sql.SQL("""
            INSERT INTO raw_measurements (
                event_id,
                timestamp,
                temperature,
                humidity,
                pressure,
                weight_seat, weight_floor,
                gas_co2, gas_ch4, gas_nox, gas_cox, gas_voc, gas_nh3,
                tof_1, tof_2, tof_3, tof_4)
            VALUES(
                {event_id},
                {timestamp},
                {temperature},
                {humidity},
                {pressure},
                {weight_seat}, {weight_floor},
                {gas_co2}, {gas_ch4}, {gas_nox}, {gas_cox}, {gas_voc}, {gas_nh3},
                {tof_1}, {tof_2}, {tof_3}, {tof_4});
        """).format(event_id=sql.Literal(event_id),
                    timestamp=sql.Literal(timestamp),
                    temperature=sql.Literal(temperature),
                    humidity=sql.Literal(humidity),
                    pressure=sql.Literal(pressure),
                    weight_seat=sql.Literal(weight_seat),
                    weight_floor=sql.Literal(weight_floor),
                    gas_co2=sql.Literal(gas_co2),
                    gas_ch4=sql.Literal(gas_ch4),
                    gas_nox=sql.Literal(gas_nox),
                    gas_cox=sql.Literal(gas_cox),
                    gas_voc=sql.Literal(gas_voc),
                    gas_nh3=sql.Literal(gas_nh3),
                    tof_1=sql.Literal(tof_1),
                    tof_2=sql.Literal(tof_2),
                    tof_3=sql.Literal(tof_3),
                    tof_4=sql.Literal(tof_4))
    sql_cursor.execute(sql_cmd)


def get_table(sql_cursor, table, columns=None):
    """
    Retrieves column data from table using sql connection cursor
    Args:
        sql_cursor: sql connection cursor from psycopg2
        table: Table name in database
        columns: List(str) Column names to retrieve from table. If left empty retrieve all columns.

    Returns:
        result Data from sql query
    """
    if columns is None:
        column_string = '*'
    else:
        column_string = ','.join(columns)

    sql_cmd = sql.SQL("""
            SELECT * FROM {table}
        """).format(  # colum_string=sql.Identifier(column_string),
                    table=sql.Identifier(table))
    sql_cursor.execute(sql_cmd)
    record = sql_cursor.fetchall()
    if not record:  # Check that a proper result value is given back
        return False
    return record


def connection_error():
    return psycopg2.Error
