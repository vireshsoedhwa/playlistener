FROM python:3.10-slim-buster as base
ENV PYTHONUNBUFFERED 1
ENV PATH /code:/opt/venv/bin:$PATH
COPY requirements.txt ./
RUN set -ex; \
        python -m venv /opt/venv; \
        pip install --upgrade pip; \
        pip install -r requirements.txt;

FROM python:3.10-slim-buster as release
ENV PYTHONUNBUFFERED 1
ENV PATH /code:/opt/venv/bin:$PATH
WORKDIR /code
RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        gdal-bin \
        libmagic1; \
    apt-get autoremove -y; \
    apt-get clean; \
    mkdir -p /run/daphne;
COPY manage.py supervisord.conf ./
COPY docker-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
COPY --from=base /root/.cache /root/.cache
COPY --from=base /opt/venv /opt/venv
COPY playlistenerapi playlistenerapi
COPY api api
EXPOSE 8000
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["supervisord", "-c", "supervisord.conf", "-n"]