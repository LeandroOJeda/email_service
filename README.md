# README

## Descripción del Proyecto

Este proyecto es una API REST para un servicio de correo electrónico que permite el envío masivo de correos electrónicos bajo un correo corporativo. El proyecto ha sido creado en Python utilizando Django como framework.

La API implementa dos servicios SMTP, lo que significa que si uno falla, el servicio de correo electrónico seguirá funcionando normalmente con el segundo servicio SMTP. Esto garantiza la alta disponibilidad y la fiabilidad del servicio de correo electrónico.

## Documentación

La documentación de la API se ha realizado con Swagger. Puedes acceder a la documentación visitando `localhost:8000/swagger/` después de iniciar el servidor.

## Cómo iniciar el servidor

Para iniciar el servidor, puedes utilizar el siguiente comando:

```bash
python manage.py runserver
```

Esto iniciará el servidor en `localhost:8000`.

## Cómo levantar el proyecto en local con Docker Compose

Si tienes Docker y Docker Compose instalados, puedes levantar el proyecto en local con el siguiente comando:

```bash
docker-compose up
```

Este comando levantará todos los servicios definidos en tu archivo `docker-compose.yml` en la raíz del proyecto. Asegúrate de estar en el directorio correcto cuando ejecutes este comando.

## Configuración de la base de datos

Deberás proporcionar la conexión a la base de datos local mediante variables de entorno. Estas variables de entorno incluyen la dirección del host de la base de datos, el nombre de la base de datos, el nombre de usuario y la contraseña. Asegúrate de tener estas variables de entorno configuradas correctamente en tu entorno local o en tu archivo `.env`.

Las variables de entorno para la base de datos generada por Docker Compose son las siguientes:

```
ENV DB_DATABASE=emailService-db
ENV DB_USR=leandro
ENV DB_PWD=password
ENV DB_HOST=db
ENV DB_PORT=3306
```
