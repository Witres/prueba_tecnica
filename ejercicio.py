from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

# Acceder a la web
options = Options()
options.add_argument('--headless')
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)
driver.get("https://www.strava.com/")

cookies = json.loads(os.getenv("STRAVA_COOKIES"))

for cookie in cookies:
    driver.add_cookie(cookie)  # Añade cada cookie a Selenium
driver.refresh()

def perfil_usuario(id):
    url=f"https://www.strava.com/athletes/{id}"
    driver.get(url)

def obtener_datos(lista_id):
    xpath_perfil="//div[@id='athlete-profile']"
    # Nombre
    def obtener_nombre():
        try:
            nombre=driver.find_element(By.XPATH,f"{xpath_perfil}//h1[contains(@class,'athlete-name')]").text
            return nombre
        except:
            print("Se ha producido un error en la búsqueda del nombre del usuario.")

    # Localizacion
    def obtener_localizacion():
        try:
            localizacion=driver.find_element(By.XPATH,f"{xpath_perfil}//div[@class='location']").text
            return localizacion
        except:
            print("Se ha producido un error en la búsqueda de la localización del usuario.")

    # Avatar
    def obtener_avatar():
        try:
            avatar=driver.find_element(By.XPATH,f"{xpath_perfil}//div[@class='avatar-img-wrapper']/img[@class='avatar-img']").get_attribute("src")
            return avatar
        except:
            print("Se ha producido un error en la búsqueda del avatar del usuario.")

    # Descripcion:(Trofeos, Logros, Actividades)
    def obtener_descripcion():
        ## Trofeos (del resumen, no todos porque suelen ser muchos)
        try:
            aux_lista_trofeos=driver.find_elements(By.XPATH,f"{xpath_perfil}//div[@id='trophy-case-summary']//li[@class='centered']")
        except:
            print("Se ha producido un error en la búsqueda de trofeos.")
        lista_trofeos=[trofeo.get_attribute("title") for trofeo in aux_lista_trofeos] 

        ## Logros
        try:
            aux_lista_logros=driver.find_elements(By.XPATH,f"{xpath_perfil}//div[@class='section athlete-achievements']//li")
        except:
            print("Se ha producido un error en la búsqueda de logros del usuario.")
        lista_logros=[]
        for elemento in aux_lista_logros:
            logro=elemento.text
            lista_logros.append(logro)

        ## Actividades (en la ultima semana)
        try:
            aux_lista_actividad=driver.find_elements(By.XPATH,f"{xpath_perfil}//div[@id='activity-log']//ul[@id='totals']//li//strong")
            [distancia,tiempo,desnivel]=aux_lista_actividad
            actividad=f"Ha hecho ejercicio durante {tiempo.text} en total. Ha recorrido {distancia.text} con un desnivel positivo de {desnivel.text}."
            return {"Trofeos" : lista_trofeos, "Logros" : lista_logros, "Actividad" : actividad}
        except:
            print("Se ha producido un error en la búsqueda de actividades del usuario.")
    informacion=[]
    for id in lista_id:
        perfil_usuario(id)
        datos_id={
            "Nombre" : obtener_nombre(),
            "Localización" : obtener_localizacion(),
            "URL del avatar" : obtener_avatar(),
            "Descripción": obtener_descripcion()
        }
        informacion.append(datos_id)
    return informacion

# Funcion obtener datos del primer usuario con nombre apellido1 apellido2
def obtener_id(nombre):
    lista_usuario_id=[]
    nombre = nombre.strip().replace(" ", "+")
    pagina=1
    while True and pagina<5 :
        lista_usuario_id.append(f"Página {pagina}")
        url=f"https://www.strava.com/athletes/search?gsf=2&page={pagina}&text={nombre}"
        driver.get(url)
        try:
            aux_list_id=driver.find_elements(By.XPATH,"//li[@class='row']//div[@class='athlete-details']//a[@class='athlete-name-link']")
            if not aux_list_id:
                break
        except:
            print("Se ha producido un error en la búsqueda de usuarios con el nombre proporcionado.")
            break
        for aux_id in aux_list_id:
            usuario=aux_id.text
            id=aux_id.get_attribute("data-athlete-id")
            lista_usuario_id.append([usuario,id])
        pagina=pagina+1
    return lista_usuario_id

# Ejercicio 1
informacion=obtener_datos([26562290, 77044008, 4196733])

## Exportar resultado del ejercicio 1 en un json   
with open("resultado1.json", "w", encoding="utf-8") as resultado:
    json.dump(informacion, resultado, ensure_ascii=False, indent=4)

# Ejercicio 2
lista_usuario_id=obtener_id("javier")

## Exportar resultado del ejercicio 2 en un json   
with open("resultado2.json", "w", encoding="utf-8") as resultado:
    json.dump(lista_usuario_id, resultado, ensure_ascii=False, indent=4)