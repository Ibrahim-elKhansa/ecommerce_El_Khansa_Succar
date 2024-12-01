FROM python:3.12-slim

WORKDIR /usr/src/app

COPY ./models ./models
COPY ./routes ./routes
COPY ./schemas ./schemas
COPY ./services ./services
COPY ./database.py ./database.py
COPY ./dependencies ./dependencies

COPY ./app_inventory/app_inventory.py ./app_inventory.py
COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app_inventory:app", "--host", "0.0.0.0", "--port", "8002"]
