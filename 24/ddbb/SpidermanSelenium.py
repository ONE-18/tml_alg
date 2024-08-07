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
from selenium.webdriver.common.keys import Keys
import sqlito
import completarBB

conn = sqlite3.connect('bb.db')
cur = conn.cursor()

# Configurar las opciones del navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless para no abrir el navegador

# Crear opciones para Microsoft Edge
edge_options = Options()
# edge_options.add_argument("--headless")  # Ejecutar en modo headless
# edge_options.add_argument("--disable-gpu")  # Desactivar la GPU para modo headless
# edge_options.add_argument("--no-sandbox")  # Deshabilitar el sandbox
edge_options.add_argument("--start-maximized")  # Maximizar la ventana del navegador

# Configurar el servicio del ChromeDriver
# service = Service(ChromeDriverManager().install()

# Iniciar el navegador
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Edge(options=edge_options)

# Array de URLs
urls = ['https://belgium.tomorrowland.com/en/line-up/?day=2024-07-19','https://belgium.tomorrowland.com/en/line-up/?day=2024-07-20','https://belgium.tomorrowland.com/en/line-up/?day=2024-07-21']

# Función para extraer datos de una URL
def extract_data(url):
    driver.get(url)
    driver.implicitly_wait(10)  # Esperar hasta 10 segundos para que los elementos se carguen
    driver.execute_script("document.body.style.zoom='50%'")

    # Scroll hacia abajo
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(10):
        body.send_keys(Keys.DOWN)
        sleep(0.3)  # Espera para cargar los elementos
        
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

def get_stage():
    # driver.get(url)
    # driver.implicitly_wait(10)  # Esperar hasta 10 segundos para que los elementos se carguen
    
    data = []
    
    # Encontrar los divs especificados
    divs = driver.find_elements(By.CSS_SELECTOR, 'div._channel_1edec_1')
    
    for div in divs:
        titulo = div.text
        
        data.append({
            'titulo': titulo,
        })
    
    return data

# Inicializa la base de datos
sqlito.IniBB()

# Lista para almacenar todos los resultados temporalmente
all_data = []

# Iterar sobre las URLs y extraer datos
for url in urls:
    data = extract_data(url)
    all_data.extend(data)
    sleep(1+random()*2)  # Esperar entre 1 y 3 segundos
# data = extract_data(urls[0])
# all_data.extend(data)

cur.execute('''DELETE FROM Escenario''')
i = 1
for escenario in get_stage():
    t = escenario['titulo']
    # print(t)
    cur.execute('''INSERT INTO Escenario (id, Nombre) VALUES (?, ?)''', (i ,t))
    conn.commit()
    i += 1

# Cerrar el navegador
driver.close()
driver.quit()

act = []

# Imprimir los resultados
for entry in all_data:
    # print(entry)
    dia = entry['url'].split('=')[1]
    comienzo = dia + " " + entry['hora'].split(' - ')[0]
    final = dia + " " + entry['hora'].split(' - ')[1]
    nombre = entry['titulo']
    h = entry['top']
    
    act.append((nombre, comienzo, final, h))

act.sort(key=itemgetter(3))

escenarios = cur.execute('SELECT * FROM Escenario').fetchall()
cur.execute('''DELETE FROM Actuación''')
i = 0

for k, gr in groupby(act, key=itemgetter(3)):
    escenario = escenarios[i][1]
    
    for a in gr:
        cur.execute('''INSERT INTO Actuación 
                (Artista, Escenario, HoraInicio, HoraFin) 
                VALUES (?, ?, ?, ?)''', (a[0], escenario, a[1], a[2]))
        conn.commit()   
    i += 1

conn.close()

completarBB.completarBB()