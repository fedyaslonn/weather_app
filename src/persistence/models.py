from sqlalchemy import ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


from datetime import datetime

class Base(DeclarativeBase):
    pass

class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    weather_predictions: Mapped[list["WeatherPrediction"]] = relationship(
        back_populates="city", cascade="all, delete-orphan", lazy="selectin")

class WeatherPrediction(Base):
    __tablename__ = "weather"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    main_detail: Mapped[str] = mapped_column(String(20), nullable=False)
    detail: Mapped[str] = mapped_column(String(100), nullable=False, comment="Текстовая информация о погоде")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="Время прогноза погоды")
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"), nullable=False)

    city: Mapped["City"] = relationship(
        back_populates="weather_predictions", lazy="joined")