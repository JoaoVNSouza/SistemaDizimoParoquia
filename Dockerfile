FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# libpq5 é necessário para o psycopg se conectar ao Postgres em runtime.
# postgresql-client fornece pg_isready (usado pelo entrypoint para aguardar o DB).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq5 \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Diretórios persistentes (serão sobrescritos por volumes no compose)
RUN mkdir -p /app/media /app/staticfiles

# Gera os estáticos já na imagem — não depende do DB
RUN SECRET_KEY=build-time DEBUG=False \
    POSTGRES_HOST=localhost POSTGRES_DB=build POSTGRES_USER=build POSTGRES_PASSWORD=build \
    python manage.py collectstatic --noinput

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
