# FROM: define la imagen BASE sobre la que construimos la nuestra.
# python:3.12-slim significa "Python 3.12 ya instalado, sobre una
# versión liviana (slim) de Linux (Debian)". Empezar desde una
# imagen slim en vez de la versión completa reduce mucho el tamaño
# final de nuestra imagen.
FROM python:3.12-slim

# Variables de entorno que afectan cómo corre Python DENTRO del
# contenedor (no tienen relación con nuestro .env de Django).
#
# PYTHONDONTWRITEBYTECODE=1: evita que Python genere archivos
# .pyc (bytecode compilado) dentro del contenedor -- no aportan
# nada útil acá y solo ensucian la imagen.
#
# PYTHONUNBUFFERED=1: hace que los print() y logs de Python
# aparezcan INMEDIATAMENTE en la terminal (en vez de acumularse
# en un buffer). Es importante para poder ver los logs de Django
# en tiempo real con "docker compose logs".
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# WORKDIR: define la carpeta de trabajo DENTRO del contenedor.
# A partir de esta línea, cualquier comando relativo (COPY, RUN)
# se ejecuta parado en /app.
WORKDIR /app

# Instalamos dependencias del SISTEMA OPERATIVO (no de Python)
# que mysqlclient necesita para funcionar en Linux. En Windows
# usamos el wheel precompilado, pero DENTRO del contenedor Linux
# necesitamos estas librerías de compilación.
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiamos SOLO el requirements.txt primero (todavía no el resto
# del código). Esto es una técnica de optimización de Docker: como
# cada instrucción del Dockerfile queda "cacheada", si después
# modificás tu código pero NO requirements.txt, Docker va a
# reutilizar la capa de "pip install" ya hecha en vez de
# reinstalar todo de cero cada vez que reconstruyas la imagen.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Recién ahora copiamos el resto del código del proyecto.
COPY . .

# EXPOSE documenta (no abre por sí solo) que este contenedor va a
# escuchar en el puerto 8000 -- el mismo que usa "runserver".
EXPOSE 8000

# CMD: el comando que se ejecuta cuando el contenedor arranca.
# 0.0.0.0 (en vez de 127.0.0.1) es importante: le dice a Django
# que escuche pedidos desde CUALQUIER dirección, no solo desde
# "sí mismo" -- necesario para que Docker pueda redirigir el
# tráfico desde tu máquina real hacia adentro del contenedor.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]