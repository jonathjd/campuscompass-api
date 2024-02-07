FROM python:3.11

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH /usr/src/app

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]