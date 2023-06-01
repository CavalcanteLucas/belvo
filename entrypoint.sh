#!/bin/bash

set -o allexport
if [ "$DOCKER" ]
then
    [[ -f .docker.env ]] && source .docker.env
else
    [[ -f .env ]] && source .env
fi
set +o allexport

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

exec "$@"