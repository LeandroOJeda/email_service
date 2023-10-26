FROM python:3.10.4-slim

WORKDIR /app/

# Copia solo los archivos necesarios para instalar las dependencias
COPY requirements-prod.txt .

ENV PYTHONUNBUFFERED 1

ENV DB_DATABASE=emailService-db
ENV DB_USR=leandro
ENV DB_PWD=password
ENV DB_HOST=db
ENV DB_PORT=3306

# Instala las dependencias y limpia después
RUN apt update && \
    apt install -y libmariadb-dev-compat gcc libmariadb-dev && \
    pip install -r requirements-prod.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia el resto de los archivos
COPY . .