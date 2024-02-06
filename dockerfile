FROM python:3.11

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH /usr/src/app

WORKDIR /usr/src/app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]