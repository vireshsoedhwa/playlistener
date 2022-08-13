# playlistenerapi

Dev:
    docker compose up
Prod:
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

    python -c "import secrets; print(secrets.token_urlsafe())"