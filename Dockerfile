# FROM python:3.10-slim-buster as base
# ENV PATH="/opt/venv/bin:/base:$PATH"
# COPY requirements.txt ./

# RUN set -ex; \
#         apt-get update; \
#         apt-get install -y --no-install-recommends \
#             build-essential \
#             ffmpeg \
#             gcc \
#         ; \
#         \
#         python -m venv /opt/venv; \
#         \
#         pip install --upgrade pip; \
#         pip install -r requirements.txt;
# # ==========================================================================================================================
# FROM node:18.1.0-slim as frontend-builder

# WORKDIR /code/frontend

# RUN set -ex; \
#         apt-get update; \
#         apt-get install -y --no-install-recommends \
#             build-essential \
#             gcc \
#             make \
#         ;

# # Create layer to install npm dependencies
# COPY frontend/package.json ./

# # # Create layer to build assets from source
# COPY frontend/public ./public
# COPY frontend/src ./src
# COPY frontend/templates ./templates
# COPY frontend/webpack.common.js ./
# COPY frontend/webpack.prod.js ./
# RUN npm install
# RUN npm run build

# ==========================================================================================================================
# Release
FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PATH /code:/opt/venv/bin:$PATH

WORKDIR /code

COPY requirements.txt ./

RUN set -ex; \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            build-essential \
            curl \
            ffmpeg \
            gcc \
            nginx \
            npm \
        ; \
        \
        python -m venv /opt/venv; \
        \
        pip install --upgrade pip; \
        pip install -r requirements.txt;

RUN apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

RUN mkdir -p /run/daphne

COPY manage.py supervisord.conf ./
COPY docker-entrypoint.sh /usr/local/bin

COPY /nginx/nginx.conf /etc/nginx/nginx.conf
COPY frontend frontend
COPY playlistener playlistener
COPY apiv1 apiv1

WORKDIR /code/frontend

RUN npm install
RUN npm run build

WORKDIR /code
EXPOSE 9000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["supervisord", "-c", "supervisord.conf", "-n"]



