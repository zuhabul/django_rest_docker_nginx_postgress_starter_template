#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

# python manage.py flush --no-input

python manage.py migrate

# you can add more commands here

# you can uncomment this line if you want to collect static files for the first time
# python manage.py collectstatic --no-input --clear
# python manage.py collectstatic --no-input

# python manage.py createsupersuer

exec "$@"
