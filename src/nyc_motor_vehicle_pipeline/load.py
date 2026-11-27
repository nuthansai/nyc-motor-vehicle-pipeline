from sqlalchemy import create_engine, URL
from sqlalchemy.exc import ArgumentError, SQLAlchemyError

from nyc_motor_vehicle_pipeline.mvc.flatten_mvc import mvc_flatten
from nyc_motor_vehicle_pipeline.open_meteo.flatten_open_meteo import weather_flatten
from nyc_motor_vehicle_pipeline.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER,DB_PORT


def load_postgres():

    try:
        url = URL.create(
            drivername='postgresql',
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME,
            port=int(DB_PORT) if DB_PORT is not None else None
        )

        mvc_df = mvc_flatten()

        weather_df = weather_flatten()
        
        engine = create_engine(url)

        with engine.begin() as conn:
            mvc_df.to_sql("raw_mvc", conn, schema="raw", if_exists="append", index=False, chunksize=1000)

            weather_df.to_sql("raw_weather", conn, schema="raw", if_exists="append", index=False, chunksize=1000)

    except ArgumentError as e:
        print(f"invalid connection URL: {e}")
        raise
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error (e.g., missing driver): {e}")
        raise

    

