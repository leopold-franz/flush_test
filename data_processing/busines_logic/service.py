from data_processing.sql_database.testing import select_all_from_raw_measurements
from data_processing.sql_database.database_manager import get_table
from data_processing.sql_database.database_manager import add_event, add_raw_measurement


def list_raw_measurements(db_connection):
    """
    List raw measurement table
    Args:
        db_connection: sql connection from psycopg2

    Returns:
        str Resulting string of raw measurement table query
    """
    #with db_connection.cursor() as db_cursor:
    #    print(get_table(db_cursor, 'users'))
    #    print(get_table(db_cursor, 'toilets'))
    #    print(get_table(db_cursor, 'events'))
    return select_all_from_raw_measurements(db_connection)


def process_raw_measurements(db_connection, data):
    """
    Process raw measurements add the to database and commit changes to database when done.

    Args:
        db_connection: sql connection from psycopg2
        data: dict Dictionary filled with data from JSON POST body

    Returns:
        str 'successful' if properly done
    """
    with db_connection.cursor() as db_cursor:
        event_id = add_event(db_cursor,
                             data['userID'],
                             data['toiletID'],
                             data['measurements'][0]['timestamp'],
                             data['measurements'][-1]['timestamp'],
                             status='done')
        # print("event_id", event_id)
        for measurement in data['measurements']:
            add_raw_measurement(db_cursor,
                                event_id,
                                measurement['timestamp'],
                                measurement['temperature'],
                                measurement['humidity'],
                                measurement['pressure'],
                                measurement['weight'][0]['seat'],
                                measurement['weight'][0]['floor'],
                                measurement['gas'][0]['CO2'],
                                measurement['gas'][0]['CH4'],
                                measurement['gas'][0]['NOX'],
                                measurement['gas'][0]['COX'],
                                measurement['gas'][0]['VOC'],
                                measurement['gas'][0]['NH3'],
                                measurement['TOF'][0]['Sensor1'],
                                measurement['TOF'][0]['Sensor2'],
                                measurement['TOF'][0]['Sensor3'],
                                measurement['TOF'][0]['Sensor4'])
    db_connection.commit()
    return 'successful'
