from typing import Protocol, Optional, Annotated, List

from src.domain.dto_models import WeatherPredictionCreation, AllCitiesWithPredictions, GetPredictionsForCity
from src.persistence.models import City, WeatherPrediction

class CityRepositoryProtocol(Protocol):
    async def add_city(self, name: str) -> City:
        ...

    async def get_all_cities_with_predictions(self) -> List[City]:
        ...

    async def get_city_by_name(self, name: str) -> Optional[City]:
        ...

class WeatherPredictionsRepositoryProtocol(Protocol):
    async def add_prediction(self, city_id: int, temperature: int, main_detail: str, detail: str) -> WeatherPrediction:
        ...

    async def get_predicts_for_city(self, city_id: int) -> List[WeatherPrediction]:
        ...

class WeatherServiceProtocol(Protocol):
    async def fetch_weather_data(self, city_name: str) -> WeatherPredictionCreation:
        ...

    async def get_query_history(self) -> AllCitiesWithPredictions:
        ...

    async def get_predictions_for_city(self, city_id: int) -> GetPredictionsForCity:
        ...
