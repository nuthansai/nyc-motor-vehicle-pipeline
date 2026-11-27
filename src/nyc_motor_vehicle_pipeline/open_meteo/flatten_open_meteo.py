import json
import pandas as pd
from nyc_motor_vehicle_pipeline.config import DATA_DIR 


def weather_flatten():      

    with open(f'{DATA_DIR}/weather_data.json','r',encoding='utf-8') as f:
        data = json.load(f)

    open_meteo_df = pd.json_normalize(data, sep='_')

    open_meteo_df['borough'] = ["MANHATTAN", "BROOKLYN", "QUEENS", "BRONX", "STATEN ISLAND"]

    open_meteo_df = open_meteo_df.explode(
        ['hourly_time', 
         'hourly_temperature_2m', 
         'hourly_rain',
         'hourly_snowfall',
         'hourly_precipitation',
         'hourly_wind_gusts_10m',
         'hourly_weather_code'
        ])

    float_columns = [ 
         'hourly_temperature_2m', 
         'hourly_rain',
         'hourly_snowfall',
         'hourly_precipitation',
         'hourly_wind_gusts_10m'
    ]

    open_meteo_df[float_columns] = open_meteo_df[float_columns].astype(float)

    open_meteo_df['hourly_weather_code'] = open_meteo_df['hourly_weather_code'].astype("Int64")

    open_meteo_df["hourly_time"] = pd.to_datetime(open_meteo_df["hourly_time"])
    
    open_meteo_df_new = open_meteo_df.drop(columns=['location_id'])

    return open_meteo_df_new




