#!/bin/sh

# Checks if the database is running before making migrations

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations main --noinput 
python manage.py migrate --noinput 

echo "Collecting static files"
python manage.py collectstatic --noinput

exec "$@"