from data_processing.flask_app.app import run_app
from data_processing.sql_database.database_manager import connect_database, close_database_connection, \
    connection_error
from data_processing.sql_database.testing import test_populate


def main():
    (connection, cursor) = (False, None)  # Initialize variables for finally clause

    try:
        #connection, cursor = connect_database(user="postgres",
        #                                      password="flush",
        #                                      host="34.65.240.155",
        #                                      port="5432",
        #                                      db_name="smarttoilet",
        #                                      verbose=True)
        connection, cursor = connect_database(user="postgres",
                                              password="testpass",
                                              host="0.0.0.0",
                                              port="8081",
                                              db_name="postgres",
                                              verbose=True)
        test_populate(cursor)
        run_app(cursor)
    except (Exception, connection_error()) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        close_database_connection(connection, cursor)


if __name__ == '__main__':
    main()
