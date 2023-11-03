FROM python:3.10.4-slim

WORKDIR /app/

COPY requirements-prod.txt .

ENV PYTHONUNBUFFERED 1


# Local Variables for Compose
# ENV DB_DATABASE=emailService-db
# ENV DB_USR=leandro
# ENV DB_PWD=password
# ENV DB_HOST=db
# ENV DB_PORT=3306

# Hosting db variables
ENV DB_DATABASE=email_service_db
ENV DB_USR=leandro
ENV DB_PWD=4jTN5zRUKW60tZb2DTZx9Db0e6X7tqud
ENV DB_HOST=dpg-cl1qap0p2gis73fjgkf0-a.oregon-postgres.render.com
ENV SPARKPOST_PASSWORD=b4933896bad38f7fff3cfd17a9515cb5dbd5c06e
ENV ELASTICEMAIL_PASSWORD=C16AE993B7056F78F1DC615A6623687665DE


RUN apt update && \
    apt-get update && \
    apt install -y libmariadb-dev-compat gcc libmariadb-dev && \
    pip install -r requirements-prod.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY . .


CMD python manage.py migrate && python manage.py runserver 0.0.0.0:80