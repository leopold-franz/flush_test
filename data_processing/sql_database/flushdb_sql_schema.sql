-- Database: smarttoilet-db, Superuser: postgres
-- Run the following to execute script from instance:
-- "psql --host=34.65.240.155 --user=postgres --password --dbname=smarttoilet -f smarttoilet_db_sql_schema.sql"
CREATE DATABASE smarttoilet ;

--
-- Name: users; Type: TABLE; Owner: flush
--

CREATE TABLE IF NOT EXISTS users (
    user_id INT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    PRIMARY KEY(user_id)
);

--
-- Name: toilets; Type: TABLE; Owner: flush
--

CREATE TABLE IF NOT EXISTS toilets (
    toilet_id INT GENERATED ALWAYS AS IDENTITY,
    type VARCHAR(10),
    address VARCHAR(255),
    location VARCHAR(255),
    status VARCHAR(10),
    PRIMARY KEY(toilet_id)
);

--
-- Name: events; Type: TABLE; Owner: flush
-- ADD FEATURES HERE
--

CREATE TABLE IF NOT EXISTS events (
    event_id INT GENERATED ALWAYS AS IDENTITY,
    user_id INT,
    toilet_id INT,
    "timestamp_start" timestamp with time zone NOT NULL,
    "timestamp_end" timestamp with time zone NOT NULL,
    status VARCHAR(10),
    PRIMARY KEY(event_id),
    CONSTRAINT fk_user
      FOREIGN KEY(user_id)
	  REFERENCES users(user_id),
	CONSTRAINT fk_toilet
      FOREIGN KEY(toilet_id)
	  REFERENCES toilets(toilet_id)
);

--
-- Name: raw_measurements; Type: TABLE; Owner: flush
--

CREATE TABLE IF NOT EXISTS raw_measurements (
    event_id int,
    "timestamp" timestamp with time zone NOT NULL,
    temperature double precision,
    humidity double precision,
    pressure double precision,
    weight_seat double precision,
    weight_floor double precision,
    gas_co2 double precision,
    gas_ch4 double precision,
    gas_nox double precision,
    gas_cox double precision,
    gas_voc double precision,
    gas_nh3 double precision,
    tof_1 double precision,
    tof_2 double precision,
    tof_3 double precision,
    tof_4 double precision,
    PRIMARY KEY (event_id, timestamp),
    CONSTRAINT fk_event
      FOREIGN KEY(event_id)
	  REFERENCES events(event_id)
);

-- If TimescaleDB would be of interest
-- SELECT create_hypertable('raw_measurements', 'timestamp', event_id, 4);


--
-- Name: events; Type: TABLE; Owner: flush
-- ADD FEATURES HERE
--

CREATE TABLE IF NOT EXISTS features (
    event_id INT,
    feature1 double precision,
    feature2 double precision,
    CONSTRAINT fk_event
      FOREIGN KEY(event_id)
	  REFERENCES events(event_id)
);