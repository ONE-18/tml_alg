from random import random
import sqlite3
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Array de URLs
urls = ['https://belgium.tomorrowland.com/en/line-up/?day=2024-07-19','https://belgium.tomorrowland.com/en/line-up/?day=2024-07-20','https://belgium.tomorrowland.com/en/line-up/?day=2024-07-21']

def down_url(url, file):
    # Crear opciones para Microsoft Edge
    edge_options = Options()
    # edge_options.add_argument("--headless")  # Ejecutar en modo headless
    # edge_options.add_argument("--disable-gpu")  # Desactivar la GPU para modo headless
    # edge_options.add_argument("--no-sandbox")  # Deshabilitar el sandbox

    # Configurar el servicio del ChromeDriver
    service = Service(EdgeChromiumDriverManager().install())

    # Iniciar el navegador
    driver = webdriver.Edge(service=service)

    driver.get(url)
    driver.implicitly_wait(10)

    source = driver.page_source

    with open(file, 'w') as f:
        f.write(source)
    # print(source)

    driver.quit()

# def parse_txt(file):

with open('source.txt', 'r', encoding='ISO-8859-1') as f:
    for line in f.readlines():
        if 'planby-program-title' in line:
            print(line)