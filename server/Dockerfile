FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./server /app

EXPOSE 8000

ENV UVICORN_CMD="uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

CMD ["sh", "-c", "$UVICORN_CMD"]

