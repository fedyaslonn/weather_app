from typing import Annotated, List
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict
from _datetime import datetime


class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class CityCreation(TunedModel):
    city_name: Annotated[str, MinLen(2), MaxLen(20)]

class CityScheme(CityCreation):
    id: int

class WeatherPredictionResponse(TunedModel):
    temperature: float
    main_detail: Annotated[str, MaxLen(20)]
    detail: Annotated[str, MaxLen(100)]
    timestamp: datetime
    city_id: int

class WeatherPredictionCreation(WeatherPredictionResponse):
    id: int

class AllCitiesWithPredictions(BaseModel):
    cities: List[CityScheme]
    predictions: List[WeatherPredictionCreation]

class GetPredictionsForCity(BaseModel):
    city_id: int
    predictions: List[WeatherPredictionCreation]