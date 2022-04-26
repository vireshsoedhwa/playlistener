FROM python:3.9.0-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN apt-get update &&  \
    apt-get upgrade -y && \
    apt-get install ffmpeg nginx -y && \
    apt-get autoremove --purge && \
    apt-get -y clean

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /nginx/nginx.conf /etc/nginx/nginx.conf

COPY apiv1 .
COPY manage.py .
COPY docker-entrypoint.sh .
RUN mkdir -p /run/daphne

EXPOSE 8000

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]