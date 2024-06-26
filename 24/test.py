from itertools import groupby
from operator import itemgetter
from random import random
import sqlite3
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import sqlito

conn = sqlite3.connect('bb.db')
cur = conn.cursor()

# Configurar las opciones del navegador
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ejecutar en modo headless para no abrir el navegador
chrome_options.add_argument("--maximized")  # Maximizar la ventana del navegador

# Crear opciones para Microsoft Edge
edge_options = Options()
# edge_options.add_argument("--headless")  # Ejecutar en modo headless
# edge_options.add_argument("--disable-gpu")  # Desactivar la GPU para modo headless
# edge_options.add_argument("--no-sandbox")  # Deshabilitar el sandbox
edge_options.add_argument("--start-maximized")  # Maximizar la ventana del navegador

# Configurar el servicio del ChromeDriver
# service = Service(ChromeDriverManager().install())
service = Service(EdgeChromiumDriverManager().install())


# Iniciar el navegador
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Edge(options=edge_options)

# Array de URLs
urls = ['https://belgium.tomorrowland.com/en/line-up/?day=2024-07-19','https://belgium.tomorrowland.com/en/line-up/?day=2024-07-20','https://belgium.tomorrowland.com/en/line-up/?day=2024-07-21']

def extract_data(url):
    driver.get(url)
    driver.implicitly_wait(10)  # Esperar hasta 10 segundos para que los elementos se carguen
    sleep(1)
    data = []
    
    # Encontrar los divs especificados
    divs = driver.find_elements(By.CSS_SELECTOR, 'div.planby-program')
    print(len(divs))
    for div in divs:
        style = div.get_attribute('style')
        top = None
        for estilo in style.split(';'):
            if 'top' in estilo:
                top = estilo.split(':')[1].strip()
        
        titulo = div.find_element(By.CSS_SELECTOR, 'p.planby-program-title').text
        hora = div.find_element(By.CSS_SELECTOR, 'span.planby-program-text').text
        
        data.append({
            'url': url,
            'top': top,
            'titulo': titulo,
            'hora': hora,
        })
    
    return data

# for data in extract_data(urls[0]):
#     if (data.get('top') == '0px'):
#         print(data)

driver.get(urls[0])
driver.implicitly_wait(10)
table = driver.find_element(By.CSS_SELECTOR, 'div.planby-content')

# Inicializar una lista para almacenar los datos de la tabla
table_data = []

# Obtener la altura y el ancho inicial de la tabla
last_height = driver.execute_script("return arguments[0].scrollHeight", table)
last_width = driver.execute_script("return arguments[0].scrollWidth", table)

while True:
    # Desplazarse hacia abajo hasta el final de la tabla
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", table)
    sleep(2)  # Esperar a que se cargue el contenido

    # Obtener la altura actual de la tabla después del desplazamiento
    new_height = driver.execute_script("return arguments[0].scrollHeight", table)

    # Desplazarse horizontalmente hacia la derecha
    while True:
        driver.execute_script("arguments[0].scrollLeft += 100", table)  # Desplazarse hacia la derecha
        sleep(2)  # Esperar a que se cargue el contenido

        # Obtener el nuevo ancho de la tabla después del desplazamiento
        new_width = driver.execute_script("return arguments[0].scrollWidth", table)

        # Obtener las filas y celdas de la tabla cargadas actualmente
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            table_data.append(row_data)

        # Verificar si el ancho de la tabla ha cambiado
        if new_width == last_width:
            break  # Si no ha cambiado, salir del bucle
        last_width = new_width

    # Verificar si la altura de la tabla ha cambiado
    if new_height == last_height:
        print('No hay cambio')
        break  # Si no ha cambiado, salir del bucle
    last_height = new_height

driver.quit()

# Mostrar los datos de la tabla
for row in table_data:
    print(row)





