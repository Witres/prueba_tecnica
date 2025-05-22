# Imagen base oficial de Python ligera
FROM python:3.11-slim

# Instala Chromium y su driver para Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    unzip \
    gnupg \
    && apt-get clean

# Variables de entorno para que Selenium encuentre el navegador y driver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código al contenedor
COPY . /app
WORKDIR /app

# Ejecuta tu script principal
CMD ["python", "ejercicio.py"]