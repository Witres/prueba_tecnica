from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()  # carga las variables del archivo .env

# Acceder a la web
driver = webdriver.Chrome()
driver.get("https://www.strava.com/")

cookies = json.loads(os.getenv("STRAVA_COOKIES"))

for cookie in cookies:
    driver.add_cookie(cookie)  # añade cada cookie a Selenium

time.sleep(20)

id=26562290
url=f"https://www.strava.com/athletes/{id}"
driver.get(url)

xpath_perfil="//div[@id='athlete-profile']"

# NOMBRE
aux_nombre=driver.find_element(By.XPATH,f"{xpath_perfil}//h1[contains(@class,'athlete-name')]")
nombre=aux_nombre.text

# Localizacion
aux_location=driver.find_element(By.XPATH,f"{xpath_perfil}//div[@class='location']")
location=aux_location.text

# Avatar
aux_avatar=driver.find_element(By.XPATH,f"{xpath_perfil}//div[@class='avatar-img-wrapper']/img[@class='avatar-img']")
avatar=aux_avatar.get_attribute("src")

# Descripcion:(Trofeos, Logros, Fotos, Actividades)
## Trofeos (del resumen, no todos porque suelen ser muchos)
aux_trofeos=driver.find_element(By.XPATH,f"{xpath_perfil}//div[@id='trophy-case-summary']") 
aux_lista_trofeos=driver.find_elements(By.XPATH,f"{xpath_perfil}//div[@id='trophy-case-summary']//li[@class='centered']") 
"""
--Si quisiera todos los trofeos, habria que usar--
aux_lista_trofeos=driver.find_elements(By.XPATH,"div[@id='trophy-case']//li[@class='centered']")
"""
lista_trofeos=[trofeo.get_attribute("title") for trofeo in aux_lista_trofeos]

## Logros
aux_logros=driver.find_element(By.XPATH,f"{xpath_perfil}//div[@class='section athlete-achievements']") 
aux_lista_logros=driver.find_elements(By.XPATH,f"{xpath_perfil}//div[@class='section athlete-achievements']//li")
logros=[]
for aux_logro in aux_lista_logros:
    logro=aux_logro.find_element(By.XPATH,".//div").text+" "+aux_logro.find_element(By.XPATH,".//a")+" ("+aux_logro.find_element(By.XPATH,".//time")+")"
    logros.append(logro)

## Actividades (en la ultima semana)
aux_actividades=driver.find_element(By.XPATH,f"{xpath_perfil}//div[@id='activity-log']")
aux_lista_actividades=aux_actividades.find_elements(By.XPATH,".//ul[@id='totals']//li//strong")
[distancia,tiempo,desnivel]=aux_lista_actividades
print(f"Ha recorrido {distancia.text} durante {tiempo} con un desnivel positivo de {desnivel}.")
    

#Funcion obtener datos de usuario con ID XXXXXXXX
def obtener_datos(id):
    url=f"https://www.strava.com/athletes/{id}"

#Funcion obtener datos de usuario con nombre apellido1 apellido2
def obtener_id(nombre):
    list_id=[]
    nombre = nombre.strip().replace(" ", "+")
    url=f"https://www.strava.com/athletes/search?gsf=2&page=1&page_uses_modern_javascript=true&text={nombre}&utf8=%E2%9C%93"
    driver.get(url)
    aux_id=driver.find_element(By.XPATH,f"//li[@class='row']//div[@class='athlete-details']//a[@class='athlete-name-link']")
    id=aux_id.get_attribute("data-athlete-id")
    list_id.append(id)
    