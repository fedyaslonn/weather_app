import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv

from src.api.endpoints.weather import weather_router
from src.config.dependencies import init_container

load_dotenv()

app = FastAPI()

container = init_container()

app.include_router(weather_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, ssl_certfile=None)