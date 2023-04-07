import asyncio
import datetime
import json
import os
import time
from statistics import mean

import aiohttp

from dotenv import load_dotenv


load_dotenv()

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
print("tomorrow:", tomorrow)  # noqa: T201
year = tomorrow.strftime("%Y")
month = tomorrow.strftime("%m")
day = tomorrow.strftime("%d")


async def get_weather_7timer(session):
    url = "http://www.7timer.info/bin/api.pl?lon=34.98&lat=48.45&product=civillight&unit=metric&output=json"

    async with session.get(url=url) as response:
        data = await response.read()
        weather = json.loads(data)
        for date_dict in weather["dataseries"]:
            if date_dict["date"] == int(f"{year}{month}{day}"):
                max_temperature = date_dict["temp2m"]["max"]
        return max_temperature


async def get_weather_open_meteo(session):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude=48.47&longitude=35.04&daily=temperature_2m_max&"
        f"start_date={year}-{month}-{day}&end_date={year}-{month}-{day}&timezone=auto"
    )

    async with session.get(url=url) as response:
        data = await response.read()
        weather = json.loads(data)
        return weather["daily"]["temperature_2m_max"][0]


async def get_weather_weatherstack(session):
    access_key = os.environ.get("ACCESS_KEY")
    url = f"http://api.weatherstack.com/current?access_key={access_key}&query=Dnipro"

    async with session.get(url=url) as response:
        data = await response.read()
        weather = json.loads(data)
        return weather["current"]["temperature"]


async def download_all_sites():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            get_weather_7timer(session),
            get_weather_open_meteo(session),
            get_weather_weatherstack(session),
        )
        print("results:", results)
        print(f"The average max temperature tomorrow will be: {round(mean(results))}")  # noqa: T201


print("Time-1", time.strftime("%X"))  # noqa: T201

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(download_all_sites())
    duration = time.time() - start_time
    print(f"Downloaded sites in {duration} seconds")  # noqa: T201

print("Time-2", time.strftime("%X"))  # noqa: T201
