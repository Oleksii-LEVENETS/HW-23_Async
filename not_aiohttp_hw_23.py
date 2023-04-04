import datetime
import os
import time
from statistics import mean

from dotenv import load_dotenv

import requests


load_dotenv()

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
print("tomorrow:", tomorrow)  # noqa: T201
year = tomorrow.strftime("%Y")
month = tomorrow.strftime("%m")
day = tomorrow.strftime("%d")


def get_weather_7timer():
    url = "http://www.7timer.info/bin/api.pl?lon=34.98&lat=48.45&product=civillight&unit=metric&output=json"

    response = requests.get(url=url)
    weather = response.json()
    for date_dict in weather["dataseries"]:
        if date_dict["date"] == int(f"{year}{month}{day}"):
            return date_dict["temp2m"]["max"]
    return 0


def get_weather_open_meteo():
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude=48.47&longitude=35.04&daily=temperature_2m_max&"
        f"start_date={year}-{month}-{day}&end_date={year}-{month}-{day}&timezone=auto"
    )

    response = requests.get(url=url)
    weather = response.json()
    return weather["daily"]["temperature_2m_max"][0]


def get_weather_weatherstack():
    access_key = os.environ.get("ACCESS_KEY")
    url = f"http://api.weatherstack.com/current?access_key={access_key}&query=Dnipro"

    response = requests.get(url=url)
    weather = response.json()
    return weather["current"]["temperature"]


def download_all_sites():
    results_1 = get_weather_7timer()
    results_2 = get_weather_open_meteo()
    results_3 = get_weather_weatherstack()
    max_temperature = round(mean([results_1, results_2, results_3]))
    print(f"The average max temperature tomorrow will be: {max_temperature}")  # noqa: T201


print("Time-1", time.strftime("%X"))  # noqa: T201

if __name__ == "__main__":
    start_time = time.time()
    download_all_sites()
    duration = time.time() - start_time
    print(f"Downloaded sites in {duration} seconds")  # noqa: T201

print("Time-2", time.strftime("%X"))  # noqa: T201
