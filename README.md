# Playlistenerapi

## Dev :
    docker compose up
    
## Prod :

    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

## The following ENV Variables need to be set for prod:
- DJANGO_SECRET_KEY
- POSTGRES_HOST
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PORT
- ADMIN_USERNAME
- ADMIN_PASSWORD

Useful commands:
    
    from django.core.management.utils import get_random_secret_key 