from nyc_motor_vehicle_pipeline.mvc.extract_mvc import download_mvc
from nyc_motor_vehicle_pipeline.open_meteo.extract_open_meteo import download_nyc_boroughs


def main():
    download_mvc()
    download_nyc_boroughs()

if __name__=="__main__":
    main()
