#!/bin/bash
set -e

echo "Ждём базу данных..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done
echo "БД готова!"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Seed только если нет пользователей
COUNT=$(python manage.py shell -c "from apps.users.models import User; print(User.objects.count())" 2>/dev/null || echo "0")
if [ "$COUNT" = "0" ]; then
  python manage.py seed_data
fi

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120

