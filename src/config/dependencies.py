from dependency_injector import containers, providers

from src.infra.repositories import CityRepository, WeatherPredictionsRepository
from src.infra.sql_repositories import SQLAlchemyRepository
from src.infra.weather_api_client import WeatherAPIClient
from src.persistence.session import get_async_session

from src.config.settings import db

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.application.service import WeatherService
from src.persistence.uow import UnitOfWork


class Container(containers.DeclarativeContainer):
    db_config = providers.Configuration()

    session_engine = providers.Singleton(
        create_async_engine,
        url=db_config.database.url,
        echo=False
    )

    async_session_factory = providers.Singleton(
        async_sessionmaker,
        bind=session_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async_session = providers.Resource(
        get_async_session,
        session_factory=async_session_factory
    )

    unit_of_work = providers.Factory(
        UnitOfWork,
        session=async_session
    )

    sql_repository = providers.Factory(
        SQLAlchemyRepository,
        session=async_session
    )

    weather_service_conf = providers.Configuration()

    weather_api_client = providers.Singleton(
        WeatherAPIClient,
        api_key=weather_service_conf.api_key
    )

    city_repository = providers.Factory(
        CityRepository,
        session=async_session
    )
    weather_repository = providers.Factory(
        WeatherPredictionsRepository,
        session=async_session
    )

    weather_service = providers.Factory(
        WeatherService,
        uow=unit_of_work,
        api_client=weather_api_client
    )

def init_container():
    container = Container()

    container.db_config.database.url.from_value(db.db_url)

    container.weather_service_conf.api_key.from_env("OPENWEATHERMAP_KEY")
    container.wire(modules=["src.api.endpoints.weather"])
    return container