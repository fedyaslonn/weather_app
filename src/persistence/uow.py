from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces import WeatherPredictionsRepositoryProtocol

from src.infra.repositories import WeatherPredictionsRepository, CityRepository


class IUnitOfWork(Protocol):
    weather: WeatherPredictionsRepositoryProtocol

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.city = CityRepository(session=self.session)
        self.weather = WeatherPredictionsRepository(session=self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
