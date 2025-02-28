from fastapi.params import Depends, Path, Query
from fastapi import HTTPException, status

from src.domain.interfaces import WeatherServiceProtocol
from src.config.dependencies import init_container, Container
from src.domain.dto_models import WeatherPredictionCreation, CityCreation, AllCitiesWithPredictions, \
    GetPredictionsForCity
from fastapi import APIRouter
from dependency_injector.wiring import Provide, inject

import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)

weather_router = APIRouter(prefix="/weather", tags=["weather"])


@weather_router.post("/fetch_weather_data", response_model=WeatherPredictionCreation)
@inject
async def fetch_weather_data(city_name: CityCreation = Query(...), service: WeatherServiceProtocol = Depends(Provide[Container.weather_service])):
    try:
        prediction = await service.fetch_weather_data(city_name.city_name)
        return prediction

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении прогноза погоды: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неожиданная ошибка при получении прогноза погоды"
        )


@weather_router.get("/query_history", response_model=AllCitiesWithPredictions)
@inject
async def get_query_history(
    service: WeatherServiceProtocol = Depends(Provide[Container.weather_service])
):
    try:
        result = await service.get_query_history()
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении истории запросов: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при получении истории запросов"
        )


@weather_router.get("/predictions/{city_id}", response_model=GetPredictionsForCity)
@inject
async def get_predictions_for_city(
    city_id: int = Path(..., description="ID города", gt=0),
    service: WeatherServiceProtocol = Depends(Provide[Container.weather_service])
):
    try:
        result = await service.get_predictions_for_city(city_id)
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении прогнозов для города с ID {city_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неожиданная ошибка при получении прогнозов"
        )
