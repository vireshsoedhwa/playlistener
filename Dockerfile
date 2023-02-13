FROM python:3.10-slim-buster as base
ENV PYTHONUNBUFFERED 1
ENV PATH /code:/opt/venv/bin:$PATH
COPY requirements.txt ./
RUN set -ex; \
        python -m venv /opt/venv; \
        pip install --upgrade pip; \
        pip install -r requirements.txt;

# ============================================ WEB ASSETS BUILDER

FROM node:19.6.0-slim as webassets-builder

WORKDIR /app

COPY app .
RUN npm install
RUN npm run build

# ============================================ Release

FROM python:3.10-slim-buster as release
ENV PYTHONUNBUFFERED 1
ENV PATH /code:/opt/venv/bin:$PATH
WORKDIR /code
ARG VERSION
ENV VERSION=${VERSION:-1.0.0}
RUN echo $VERSION > .env

RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        gdal-bin \
        nginx \
        curl \
        libmagic1; \
    apt-get autoremove -y; \
    apt-get clean; 

RUN set -ex; \
    curl -fsSL https://deb.nodesource.com/setup_19.x | bash - && \
    apt-get install -y nodejs

COPY manage.py .
COPY docker-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
COPY --from=base /root/.cache /root/.cache
COPY --from=base /opt/venv /opt/venv
COPY --from=webassets-builder /app/build ./app/build

COPY playlistenerapi playlistenerapi
COPY app app

COPY nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 8000
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8001", "--forwarded-allow-ips=*", "playlistenerapi.wsgi"]