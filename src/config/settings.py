import os
from dataclasses import dataclass
from dotenv import load_dotenv
import sys
from pydantic import BaseModel
from pydantic.v1 import BaseSettings, Field

load_dotenv()

class DBSettings(BaseSettings):
    host: str = Field(..., env="DB_HOST")
    port: int = Field(5432, env="DB_PORT")
    user: str = Field(..., env="DB_USER")
    password: str = Field(..., env="DB_PASS")
    name: str = Field(..., env="DB_NAME")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

db = DBSettings()