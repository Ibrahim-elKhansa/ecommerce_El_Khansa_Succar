FROM python:3.12-slim

WORKDIR /usr/src/app

COPY ./models ./models
COPY ./routes ./routes
COPY ./database.py ./database.py

COPY ./app_sales/app_sales.py ./app_sales.py
COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app_sales:app", "--host", "0.0.0.0", "--port", "8000"]
