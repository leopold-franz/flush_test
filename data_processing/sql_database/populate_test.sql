-- Database: smarttoilet-db, Superuser: postgres
-- Run the following to execute script from instance:
-- "psql --host=34.65.240.155 --user=postgres --password --dbname=smarttoilet -f populate_test.sql"

--
-- Insert user
--

INSERT INTO users (first_name, last_name, date_of_birth)
VALUES('leopold', 'franz', '1997-01-13');

--
-- Insert toilet
--

INSERT INTO toilets (type, address, location, status)
VALUES('flush-1', 'Schmelzbergstrasse 26', 'First Floor', 'active');

--
-- Insert event
--

INSERT INTO events (user_id, toilet_id, timestamp_start, timestamp_end, status)
VALUES(1, 1, (SELECT CURRENT_TIMESTAMP), (SELECT CURRENT_TIMESTAMP), 'active')
RETURNING event_id;

--
-- Insert measurement
--

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
    1,
    (SELECT CURRENT_TIMESTAMP),
    21.5,
    39.4,
    1,
    4,3,
    6,6,6,6,6,6,
    2,2,2,2);

