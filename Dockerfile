FROM python:3.10-slim-buster as base

ENV PATH="/opt/venv/bin:/base:$PATH"

COPY requirements.txt ./

RUN set -ex; \
        apt-get update; \
        apt-get install -y --no-install-recommends \
            build-essential \
            gcc \
        ; \
        \
        python -m venv /opt/venv; \
        \
        pip install --upgrade pip; \
        pip install -r requirements.txt;



# FROM python:3.9.0-slim AS base
# ENV PYTHONUNBUFFERED 1
# WORKDIR /code

# RUN apt-get update &&  \
#     apt-get upgrade -y && \
#     apt-get install ffmpeg nginx build-essential -y && \
#     apt-get autoremove --purge && \
#     apt-get -y clean

# RUN pip install --upgrade pip

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Create layer to install npm dependencies
# COPY frontend/package.json .
# RUN npm install

# # Create layer to build assets from source
# COPY frontend/public ./public
# COPY frontend/src ./src
# COPY frontend/templates ./templates
# COPY frontend/webpack.common.js .
# COPY frontend/webpack.prod.js .
# COPY frontend/package.json .
# RUN npm run build
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Release
FROM python:3.10-alpine AS release

ENV PYTHONUNBUFFERED 1
ENV PATH /code:/opt/venv/bin:$PATH

WORKDIR /code

RUN apk --update add npm \
    nginx; \
    chmod -R 755 /var/lib/nginx \
    ;

RUN mkdir -p /run/daphne

COPY manage.py supervisord.conf ./
COPY docker-entrypoint.sh /usr/local/bin

COPY --from=base /root/.cache /root/.cache
COPY --from=base /opt/venv /opt/venv

# COPY --from=frontend-builder /code/frontend/static ./frontend/static
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

COPY frontend frontend/

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 9000
CMD ["supervisord", "-c", "supervisord.conf", "-n"]


# COPY apiv1 .
# COPY manage.py .
# COPY docker-entrypoint.sh .
# RUN mkdir -p /run/daphne

# EXPOSE 8000

# RUN chmod +x ./docker-entrypoint.sh

# ENTRYPOINT ["./docker-entrypoint.sh"]