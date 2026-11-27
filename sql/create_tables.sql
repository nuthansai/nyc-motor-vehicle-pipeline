CREATE SCHEMA IF NOT EXISTS raw;

-- Creating table for the NYC Motor Vehicle Collisions dataset

CREATE TABLE IF NOT EXISTS raw.raw_mvc (
    collision_id VARCHAR(50) NOT NULL PRIMARY KEY ,
    crash_date TIMESTAMP,
    crash_time TIME,
    borough VARCHAR(50),
    zip_code VARCHAR(10),
    latitude FLOAT,
    longitude FLOAT,
    on_street_name VARCHAR(100),
    cross_street_name VARCHAR(100),
    number_of_persons_injured INT,
    number_of_persons_killed INT,
    number_of_pedestrians_injured INT,
    number_of_pedestrians_killed INT,
    number_of_cyclist_injured INT,
    number_of_cyclist_killed INT,
    number_of_motorist_injured INT,
    number_of_motorist_killed INT,
    off_street_name VARCHAR(100),
    contributing_factor_vehicle_1 VARCHAR(255),
    vehicle_type_code_1 VARCHAR(100),
    contributing_factor_vehicle_2 VARCHAR(255),
    vehicle_type_code_2 VARCHAR(100),
    contributing_factor_vehicle_3 VARCHAR(255), 
    vehicle_type_code_3 VARCHAR(100),
    contributing_factor_vehicle_4 VARCHAR(255),
    vehicle_type_code_4 VARCHAR(100), 
    contributing_factor_vehicle_5 VARCHAR(255),
    vehicle_type_code_5 VARCHAR(100),
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Creating table for the Open Meteo weather dataset

CREATE TABLE IF NOT EXISTS raw.raw_weather (
    borough VARCHAR(50) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    generationtime_ms FLOAT,   
    utc_offset_seconds INT,
    timezone VARCHAR(50),
    timezone_abbreviation VARCHAR(10),
    elevation FLOAT,
    hourly_units_time VARCHAR(50),
    hourly_units_temperature_2m VARCHAR(10),
    hourly_units_rain VARCHAR(10),
    hourly_units_snowfall VARCHAR(10),
    hourly_units_wind_gusts_10m VARCHAR(10),
    hourly_units_precipitation VARCHAR(10),
    hourly_units_weather_code VARCHAR(10),
    hourly_time TIMESTAMP NOT NULL,
    hourly_temperature_2m FLOAT,
    hourly_rain FLOAT,
    hourly_snowfall FLOAT,
    hourly_wind_gusts_10m FLOAT,
    hourly_precipitation FLOAT,
    hourly_weather_code INT,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (borough, hourly_time)
);