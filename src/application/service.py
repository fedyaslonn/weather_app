from datetime import datetime

from src.domain.dto_models import WeatherPredictionCreation, AllCitiesWithPredictions, GetPredictionsForCity, CityScheme
from src.infra.weather_api_client import WeatherAPIClientProtocol
from src.persistence.uow import IUnitOfWork

from fastapi import HTTPException, status

import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, uow: IUnitOfWork,  api_client: WeatherAPIClientProtocol):
        self.uow = uow
        self.api_client = api_client

    async def fetch_weather_data(self, city_name: str) -> WeatherPredictionCreation:
        async with self.uow as uow:
            search_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось сделать прогноз погоды"
            )
            try:
                city = await uow.city.add_city(name=city_name)

                coordinates = await self.api_client.get_coordinates(city_name)
                if not coordinates:
                    logger.error(f"Город '{city_name}' не найден")
                    raise ValueError(f"Город '{city_name}' не найден")


                logger.info(f"Ответ от апишки: {coordinates}")

                current_time = int(datetime.utcnow().timestamp())

                logger.info(f"{current_time}")

                weather_data = await self.api_client.get_weather_data(lat=coordinates["lat"], lon=coordinates["lon"], dt=current_time)

                logger.info(f"Ответ от апишки: {weather_data}")

                if not weather_data or "weather" not in weather_data:
                    logger.error(f"Нет данных о погоде {weather_data}")
                    raise ValueError("Нет данных о погоде")

                temperature = weather_data["main"]["temp"]
                main_detail = weather_data["weather"][0]["main"]
                detail = weather_data["weather"][0]["description"]

                prediction = await uow.weather.add_prediction(
                    city_id=city.id,
                    temperature=temperature,
                    main_detail=main_detail,
                    detail=detail
                )

                prediction_response = WeatherPredictionCreation(
                    id=prediction.id,
                    temperature=prediction.temperature,
                    main_detail=prediction.main_detail,
                    detail=prediction.detail,
                    timestamp=prediction.timestamp,
                    city_id=prediction.city_id
                )

                await uow.commit()

            except HTTPException as e:
                logger.error(f"Ошибка при попытке сделать прогноз {e.detail}")
                await uow.rollback()
                raise search_exception

            except Exception as e:
                logger.error(f"Ошибка: {str(e)}")
                await uow.rollback()
                raise e

            return prediction_response

    async def get_query_history(self) -> AllCitiesWithPredictions:
        async with self.uow as uow:
            search_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось получить города со всеми их прогнозами"
            )
            try:
                result = await uow.city.get_all_cities_with_predictions()

                cities = [
                    CityScheme(id=city.id, city_name=city.name)
                    for city in result
                ]

                predictions = [
                    WeatherPredictionCreation(
                        id=prediction.id,
                        temperature=prediction.temperature,
                        main_detail=prediction.main_detail,
                        detail=prediction.detail,
                        timestamp=prediction.timestamp,
                        city_id=prediction.city_id
                    )
                    for city in result
                    for prediction in city.weather_predictions
                ]

                result_response = AllCitiesWithPredictions(cities=cities, predictions=predictions)

            except HTTPException as e:
                logger.error(f"Ошибка при попытке получить города со всеми прогнозами {e.detail}")
                raise search_exception

            except Exception as e:
                logger.error(f"Ошибка: {str(e)}")
                raise e

            return result_response

    async def get_predictions_for_city(self, city_id: int) -> GetPredictionsForCity:
        async with self.uow as uow:
            search_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не получить все прогнозы для города"
            )
            try:
                result = await uow.weather.get_predicts_for_city(city_id)
                predictions = [
                    WeatherPredictionCreation(
                        id=prediction.id,
                        temperature=prediction.temperature,
                        main_detail=prediction.main_detail,
                        detail=prediction.detail,
                        timestamp=prediction.timestamp,
                        city_id=prediction.city_id
                    )
                    for prediction in result
                ]

                result_response = GetPredictionsForCity(city_id=city_id, predictions=predictions)

            except HTTPException as e:
                logger.error(f"Ошибка при попытке все прогнозы для города {e.detail}")
                raise search_exception

            except Exception as e:
                logger.error(f"Ошибка: {str(e)}")
                raise e

            return result_response