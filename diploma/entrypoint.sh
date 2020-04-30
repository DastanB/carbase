#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


python manage.py flush --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'dastan211298@gmail.com', 'pass')"


exec "$@"
