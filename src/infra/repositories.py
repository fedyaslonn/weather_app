from typing import List, Optional

from src.infra.sql_repositories import SQLAlchemyRepository
from src.persistence.models import City, WeatherPrediction

from sqlalchemy.orm import selectinload
from sqlalchemy import select

class CityRepository(SQLAlchemyRepository):
    model = City

    async def add_city(self, name: str) -> City:
        existing_city = await self.get_city_by_name(name)

        if not existing_city:
            return await self.add_one({"name": name})

        return existing_city

    async def get_all_cities_with_predictions(self) -> List[City]:
        stmt = select(City).options(selectinload(City.weather_predictions))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_city_by_name(self, name: str) -> Optional[City]:
        stmt = select(City).where(City.name == name)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

class WeatherPredictionsRepository(SQLAlchemyRepository):
    model = WeatherPrediction

    async def add_prediction(self, city_id: int, temperature: int, main_detail: str, detail: str) -> WeatherPrediction:
        return await self.add_one({"city_id": city_id, "temperature": temperature, "main_detail": main_detail, "detail": detail})

    async def get_predicts_for_city(self, city_id: int) -> List[WeatherPrediction]:
        stmt = select(WeatherPrediction).where(WeatherPrediction.city_id == city_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()