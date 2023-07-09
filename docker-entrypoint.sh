#!/bin/sh

set -e
# tail -f /dev/null
if [ -z "${DJANGO_SECRET_KEY}" ];then
  echo DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY >> .env
fi

mkdir -p /code/logs
mkdir -p /code/data
# tail -f /dev/null
touch /code/logs/task.log
touch /code/logs/celery.log
cat /dev/null > /code/logs/task.log
cat /dev/null > /code/logs/celery.log

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

# celery -A playlistenerapi worker --loglevel=debug --detach worker_hijack_root_logger=False worker_redirect_stdouts_level=DEBUG

celery -A playlistenerapi worker --detach --loglevel=DEBUG --concurrency=2 -n worker1@%h worker_hijack_root_logger=False worker_redirect_stdouts=False worker_redirect_stdouts_level=DEBUG

celery -A playlistenerapi beat --detach --loglevel=DEBUG --scheduler django_celery_beat.schedulers:DatabaseScheduler

>&2 echo "Starting Nginx..."
nginx

>&2 echo "Starting app..."
exec "$@"