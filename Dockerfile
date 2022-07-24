FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PATH /code:/opt/venv/bin:$PATH

WORKDIR /code

COPY requirements.txt ./

RUN set -ex; \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            build-essential \
            ffmpeg \
            # curl \
            # gcc \
            # nginx \
        ; \
        python -m venv /opt/venv; \
        pip install --upgrade pip; \
        pip install -r requirements.txt;

RUN mkdir -p /run/daphne

COPY manage.py supervisord.conf ./
COPY docker-entrypoint.sh /usr/local/bin

# COPY /nginx/nginx.conf /etc/nginx/nginx.conf
COPY playlistener playlistener
# COPY frontend frontend
COPY api api

EXPOSE 9000
EXPOSE 9001

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["supervisord", "-c", "supervisord.conf", "-n"]
# CMD ["daphne", "-b", "0.0.0.0", "-p", "9001", "playlistener.asgi:application"]
# CMD ["nginx", "-g", "daemon off;"]

