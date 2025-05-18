from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time

# Acceder a la web
driver = webdriver.Chrome()
driver.get("https://www.strava.com/")

# driver.find_element(By.XPATH,"//div[@class='cdk-overlay-pane' and contains(@id,'cdk-overlay')]//mat-dialog-container[contains(@id,'mat-dialog-')]//h1[contains(text(),'Trade Not Confirmed')]")

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

#Funcion obtener datos de usuario con ID XXXXXXXX
def obtener_datos_id(id):
    url=f"https://www.strava.com/athletes/{id}"

#Funcion obtener datos de usuario con nombre apellido1 apellido2
def obtener_datos_nombre(nombre):
    url=f"https://www.strava.com/athletes/search?gsf=2&page=1&page_uses_modern_javascript=true&text={nombre}&utf8=%E2%9C%93"