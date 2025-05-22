# prueba_tecnica
Scrapea la web Strava para obtener información de perfiles.

- Inicia el webdriver en modo headless para realizar dos posibles acciones:
    - Obtener datos de los perfiles cuyos ids estan en la lista proporcionada (Nombre, Localizacion, URL del avatar y Descripcion -Trofeos, Logros y Actividad-)
    - Obtener el nombre e id de los usuarios que aparezcan en la busqueda con el nombre proporcionado, devolviendo una lista de elementos [nombre,id].
- Uso de cookies para autenticación alamacenadas en .env 

Instala las dependencias con:
```bash
pip install -r requirements.txt
```

Comando para correr la imagen:
```bash
docker build -t strava-scraper .
```

Comando para obtener json de output:
```bash
docker run --rm -v ruta-local/output:/app/output strava-scraper
```