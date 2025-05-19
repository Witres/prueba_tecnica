from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time

# Acceder a la web
driver = webdriver.Chrome()
driver.get("https://www.strava.com/")
