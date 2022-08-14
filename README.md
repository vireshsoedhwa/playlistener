# Playlistenerapi

## Dev :
    docker compose up

## Prod :

    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

## The following ENV Variables need to be set for prod:
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- ADMIN_USERNAME=
- ADMIN_PASSWORD=
- DJANGO_SECRET_KEY=

Useful commands:
    
    from django.core.management.utils import get_random_secret_key 