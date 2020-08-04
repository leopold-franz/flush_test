# To install psycopg2
# 1. sudo apt-get install libpq-dev
# 2. pip install psycopg2
from data_processing.sql_database.database_manager import *
from datetime import datetime


def select_all_from_raw_measurements(sql_cursor):
    """
    Test to check if database data retrieval works
    Args:
        sql_cursor: sql connection cursor from psycopg2

    Returns:
        result Result from database query
    """
    return get_table(sql_cursor, 'raw_measurements')


def test_populate(sql_cursor):
    """
    Function to test population of database with dummy data
    Args:
        sql_cursor: sql connection cursor from psycopg2

    Returns:
        None
    """
    user_id = add_user(sql_cursor, 'leopold', 'franz', '1997-01-13')

    toilet_id = add_toilet(sql_cursor, 'flush-02', 'Schmelzbergstrasse 26, 8006 Zurich, Schweiz', 'first floor', 'active')

    event_id = add_event(sql_cursor, user_id, toilet_id, str(datetime.now()), str(datetime.now()), 'done')
    print(event_id)

    add_raw_measurement(sql_cursor, event_id, str(datetime.now()), 37.5, 40, 1, 60, 20, 8, 8, 8, 8, 8, 8, 2, 2, 2, 2)


def main():
    (connection, cursor) = (False, None)  # Initialize variables for finally clause

    try:
        connection, cursor = connect_database(user="postgres",
                                              password="flush",
                                              host="34.65.240.155",
                                              port="5432",
                                              db_name="smarttoilet",
                                              verbose=True)
        test_populate(cursor)
    except (Exception, connection_error()) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        close_database_connection(connection, cursor)


if __name__ == '__main__':
    main()
