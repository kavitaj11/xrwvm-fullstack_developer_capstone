FROM python:3.12-slim-bookworm

WORKDIR /app

# Install only required system libs (Postgres + build tools for psycopg)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoapp.wsgi:application"]
