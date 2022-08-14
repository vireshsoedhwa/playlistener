#!/bin/sh

set -e

touch .env
> .env
echo DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY >> .env

if [[ -z "${GO_PIPELINE_LABEL}" ]]; then
  echo GO_PIPELINE_LABEL=$GO_PIPELINE_LABEL >> .env
else
  echo GO_PIPELINE_LABEL=dev >> .env
fi

>&2 echo "Make Database migrations"
python manage.py makemigrations api
echo "-------------------------------------------------------------------------------------------\n"

>&2 echo "Run Database migrations"
python manage.py migrate
echo "-------------------------------------------------------------------------------------------\n"

# Collect static files
>&2 echo "Collect static"
python manage.py collectstatic --noinput

>&2 echo "Start Django Q task Scheduler"
python manage.py qcluster &
echo "-------------------------------------------------------------------------------------------\n"

>&2 echo "Create superuser 'admin'"
echo "from django.contrib.auth.models import User; \
        User.objects.filter(username='$ADMIN_USERNAME').exists() or \
        User.objects.create_superuser('$ADMIN_USERNAME', 'admin@example.com', '$ADMIN_PASSWORD');" \
    | python /code/manage.py shell
echo "-------------------------------------------------------------------------------------------\n"

>&2 echo "Starting supervisor..."
exec "$@"