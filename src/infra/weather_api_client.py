import aiohttp

from typing import Protocol, Optional

import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class WeatherAPIClientProtocol(Protocol):
    async def get_coordinates(self, city: str) -> Optional[dict]:
        ...

    async def get_weather_data(self, lat: float, lon: float, dt: int) -> Optional[dict]:
        ...

class WeatherAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    async def get_coordinates(self, city: str) -> Optional[dict]:
        params = {
            "q": city,
            "appid": self.api_key,
            "limit": 1
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.openweathermap.org/geo/1.0/direct", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
                return None

    async def get_weather_data(self, lat: float, lon: float, dt: int) -> Optional[dict]:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "appid": self.api_key,
            "units": "metric",
            "lang": "ru"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()

                    logger.info(f"Данные прогноза - {data}")

                    if "weather" and "main" in data:
                        return data

                    else:
                        return None

                return None