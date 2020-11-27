FROM python:3.8.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && useradd -M gunicorn
COPY . .

USER gunicorn

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--bind=:8000", "--workers=2", "server:app"]
