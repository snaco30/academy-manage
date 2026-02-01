#!/bin/sh

# Wait for postgres
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run migrations
python manage.py migrate
python manage.py collectstatic --no-input

# Start Gunicorn
exec gunicorn academy_project.wsgi:application --bind 0.0.0.0:8000
