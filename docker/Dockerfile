FROM python:3.10-slim
WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y curl && \
    pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 python - && \
    apt-get remove -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/root/.local/bin"
RUN poetry --version

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install -r requirements.txt

COPY src/ ./src
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]