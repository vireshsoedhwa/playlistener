#!/bin/sh

set -e
# tail -f /dev/null
if [ -z "${DJANGO_SECRET_KEY}" ];then
  echo DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY >> .env
fi

>&2 echo "Make Database migrations"
python manage.py makemigrations app
echo "-------------------------------------------------------------------------------------------\n"

>&2 echo "Run Database migrations"
python manage.py migrate
echo "-------------------------------------------------------------------------------------------\n"

mkdir -p /code/app/build/static

# Collect static files
>&2 echo "Collect static"
python manage.py collectstatic --noinput

# >&2 echo "Start Django Q task Scheduler"
# python manage.py qcluster &
# echo "-------------------------------------------------------------------------------------------\n"

>&2 echo "Starting Nginx..."
nginx

>&2 echo "Starting app..."
exec "$@"