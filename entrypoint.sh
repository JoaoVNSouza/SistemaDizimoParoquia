#!/bin/sh
set -e

# Aguarda o Postgres ficar pronto (depends_on healthcheck já cobre, mas
# isto protege cenários onde o web é iniciado sozinho ou fora do compose).
if [ -n "$POSTGRES_HOST" ]; then
    echo ">> Aguardando Postgres em ${POSTGRES_HOST}:${POSTGRES_PORT:-5432}..."
    until pg_isready -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-dizimo}" >/dev/null 2>&1; do
        sleep 1
    done
    echo ">> Postgres pronto."
fi

echo ">> Aplicando migrações..."
python manage.py migrate --noinput

# Cria superusuário automaticamente se variáveis estiverem setadas
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo ">> Garantindo superusuário $DJANGO_SUPERUSER_USERNAME..."
    python manage.py createsuperuser --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" || true
fi

exec "$@"
