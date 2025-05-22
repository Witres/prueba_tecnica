from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Union

load_dotenv()  # Carga las variables del archivo .env

class ScraperStrava:
    def __init__(self) -> None:
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=self.options) # Inicia el driver con la configuracion deseada
        self.driver.get("https://www.strava.com/") # Accede a la web
        self.cookie = json.loads(os.getenv("COOKIES"))[0]
        self.driver.add_cookie(self.cookie)  # Añade la cookie a Selenium

    def perfil_usuario(self, id : int) -> None: # Accede al perfil del usuario con el id determinado
        url=f"https://www.strava.com/athletes/{id}"
        self.driver.get(url)
        if not (self.driver.current_url == url or self.driver.current_url == f"https://www.strava.com/pros/{id}"):
            print(f"No se ha encontrado el usuario con id {id}.")

    def obtener_nombre(self) -> str: # Obtiene el nombre del perfil actual
        try:
            nombre = self.driver.find_element(By.XPATH,"//div[@id='athlete-profile']//h1[contains(@class,'athlete-name')]").text
        except Exception as e:
            nombre = f"Se ha producido un error en la búsqueda del nombre del usuario: {e}"
        return nombre

    def obtener_localizacion(self) -> str: # Obtiene la localizacion del perfil actual
        try:
            localizacion = self.driver.find_element(By.XPATH,"//div[@id='athlete-profile']//div[@class='location']").text
        except Exception as e:
            localizacion = f"Se ha producido un error en la búsqueda de la localización del usuario: {e}"
        return localizacion

    def obtener_avatar(self) -> str: # Obtiene la ruta a la imagen del avatar del perfil actual
        try:
            avatar=self.driver.find_element(By.XPATH,"//div[@id='athlete-profile']//div[@class='avatar-img-wrapper']//img[@class='avatar-img']").get_attribute("src")
        except Exception as e:
            avatar = f"Se ha producido un error en la búsqueda del avatar del usuario: {e}"
        return avatar

    
    def obtener_descripcion(self) -> Dict[str, Union[List[str], str]]: # Obtiene la descripcion (Trofeos, Logros, Actividades) del perfil actual
        # Trofeos (del resumen, no todos porque suelen ser muchos)
        try:
            aux_lista_trofeos=self.driver.find_elements(By.XPATH,"//div[@id='athlete-profile']//div[@id='trophy-case-summary']//li[@class='centered']")
            if not aux_lista_trofeos:
                lista_trofeos = ["Este usuario no tiene trofeos"]
            else:
                lista_trofeos=[trofeo.get_attribute("title") for trofeo in aux_lista_trofeos] 
        except Exception as e:
            lista_trofeos = [f"Se ha producido un error en la búsqueda de trofeos: {e}"]

        # Logros
        try:
            aux_lista_logros=self.driver.find_elements(By.XPATH,"//div[@id='athlete-profile']//div[@class='section athlete-achievements']//li")
            if not aux_lista_logros:
                lista_logros = ["Este usuario no tiene logros"]
            else:
                lista_logros=[]
                for elemento in aux_lista_logros:
                    logro=elemento.text
                    lista_logros.append(logro)
        except Exception as e:
            lista_logros = [f"Se ha producido un error en la búsqueda de logros del usuario: {e}"]

        # Actividades (en la ultima semana)
        try:
            aux_lista_actividad=self.driver.find_elements(By.XPATH,"//div[@id='athlete-profile']//div[@id='activity-log']//ul[@id='totals']//li//strong")
            if not aux_lista_actividad:
                aux_lista_actividad = ["No se ha encontrado actividad de este usuario", "", ""]
            else:
                [distancia,tiempo,desnivel] = aux_lista_actividad
            actividad=f"Ha hecho ejercicio durante {tiempo.text} en total. Ha recorrido {distancia.text} con un desnivel positivo de {desnivel.text}."
        except:
            actividad = "Se ha producido un error en la búsqueda de actividades del usuario."
        return {"Trofeos" : lista_trofeos, "Logros" : lista_logros, "Actividad" : actividad}

    def obtener_datos(self,lista_id : List[int]) -> List[Dict[str, Union[str, Dict[str, Union[List[str], str]]]]]: # Dada una lista de ids, extrae la informacion de cada uno y la almacena en diccionarios
        informacion=[]
        for id in lista_id:
            self.perfil_usuario(id)
            datos_id={
                "Nombre" : self.obtener_nombre(),
                "Localización" : self.obtener_localizacion(),
                "URL del avatar" : self.obtener_avatar(),
                "Descripción": self.obtener_descripcion()
            }
            informacion.append(datos_id)
        return informacion

    def obtener_id(self, nombre : str) -> List[Union[str, List[Union[str, int]]]]: # Obtiene el nombre e id de los usuarios que aparezcan en la busqueda con el nombre proporcionado
        lista_usuario_id=[]
        nombre = nombre.strip().replace(" ", "+")
        pagina=1
        while pagina<5 : # Busca hasta la pagina 4 (incluida) para evitar que tarde demasiado
            url=f"https://www.strava.com/athletes/search?query={nombre}&page={pagina}"
            self.driver.get(url)
            try:
                aux_list_id=self.driver.find_elements(By.XPATH,"//li[@class='AthleteList_athleteListItem__egbVo']//div[@class='Athlete_athleteInfo__rVPKN']//a")
                if not aux_list_id:
                    break
                lista_usuario_id.append(f"Página {pagina}")
            except:
                print(f"Se ha producido un error en la página {pagina} de la búsqueda de usuarios con el nombre proporcionado.")
                break
            for aux_id in aux_list_id:
                usuario=aux_id.text
                id=aux_id.get_attribute("href").split("/")[-1]
                lista_usuario_id.append([usuario,id])
            pagina=pagina+1
        return lista_usuario_id

scraper = ScraperStrava()

informacion=scraper.obtener_datos([26562290, 77044008, 4196733, 168489713])
lista_usuario_id=scraper.obtener_id("javier")

# EJERCICIO 1
print(json.dumps(informacion, indent=4, ensure_ascii=False))
# EJERCICIO 2
print(json.dumps(lista_usuario_id, indent=4, ensure_ascii=False))

"""
# Exportar resultado del ejercicio 1 en un json   
# with open("/app/output/resultado1.json", "w", encoding="utf-8") as resultado:
#     json.dump(informacion, resultado, ensure_ascii=False, indent=4)


# Exportar resultado del ejercicio 2 en un json   
# with open("/app/output/resultado2.json", "w", encoding="utf-8") as resultado:
#     json.dump(lista_usuario_id, resultado, ensure_ascii=False, indent=4)
"""