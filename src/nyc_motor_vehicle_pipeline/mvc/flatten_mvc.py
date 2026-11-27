import json
import pandas as pd
from nyc_motor_vehicle_pipeline.config import DATA_DIR 


def mvc_flatten():
    with open(f'{DATA_DIR}/mvc_crashes_data.json', 'r') as f:
        data = json.load(f)

    mvc_df = pd.json_normalize(data, sep='_')

    float_columns = ['latitude', 'longitude']

    int_columns = [
        'number_of_persons_injured', 
        'number_of_persons_killed',
        'number_of_pedestrians_injured',
        'number_of_pedestrians_killed',
        'number_of_cyclist_injured',
        'number_of_cyclist_killed',
        'number_of_motorist_injured',
        'number_of_motorist_killed'
    ]

    mvc_df[float_columns] = mvc_df[float_columns].astype(float)

    mvc_df[int_columns] = mvc_df[int_columns].astype("Int64")

    mvc_df["crash_date"] = pd.to_datetime(mvc_df["crash_date"])
    mvc_df["crash_time"] = pd.to_datetime(mvc_df["crash_time"], format="%H:%M").dt.time

    mvc_df = mvc_df.drop(columns=[':id', ':version', ':created_at', ':updated_at', 'location_latitude', 'location_longitude', 'location_human_address'])

    mvc_df_new = mvc_df.rename(columns={'vehicle_type_code1': 'vehicle_type_code_1', 'vehicle_type_code2' : 'vehicle_type_code_2'})

    return mvc_df_new