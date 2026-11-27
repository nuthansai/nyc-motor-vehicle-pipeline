from nyc_motor_vehicle_pipeline.mvc.extract_mvc import download_mvc
from nyc_motor_vehicle_pipeline.open_meteo.extract_open_meteo import download_nyc_boroughs
from nyc_motor_vehicle_pipeline.load import load_postgres


def main():
    # download_mvc()
    # download_nyc_boroughs()
    load_postgres()

if __name__=="__main__":
    main()
