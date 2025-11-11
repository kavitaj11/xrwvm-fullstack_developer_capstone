FROM python:3.12.0-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV APP=/app
WORKDIR $APP

# Install system dependencies for psycopg2, mysqlclient, etc
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt $APP/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code (including templates)
COPY . $APP/

# Permissions
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# ✅ FIX: reference correct project name (`server`)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]
