from datetime import datetime, timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup

def generar_url():
    url = 'https://www.tomorrowland.com/en/festival/line-up?weekend=W1&day=19/07/2024'
    
    url_base = url[:-10] 

    fecha = datetime.strptime(url[-10:], '%d/%m/%Y')

    for i in range(6):
        if i == 3:
            url_base = url_base.replace('W1', 'W2')
            fecha = fecha + timedelta(days=4)
        
        url = url_base + (fecha + timedelta(days=i)).strftime('%d/%m/%Y')
    
        yield url

def descargar_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong:",err)


def descargarLineUp(texto):
    empezar = False
    ret = []
    for line in texto.split('\n'):
        if empezar:
            for art in line.split(' • '):
                ret.append(art)
        if 'ARTISTS' == line:
            empezar = True
    return ret

def scrap():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_experimental_option('detach', False)
    
    driver = webdriver.Chrome(options=options)
    
    wait = WebDriverWait(driver, 10)
    
    lineUp = []
    
    for url in generar_url():      # iterar entre los 2 fines de semana
        
        driver.get(url)
        sleep(1)
        t = wait.until(EC.presence_of_element_located((By.XPATH, '//tml-lineup'))).text
        
        for art in descargarLineUp(t):
            if art not in lineUp:
                lineUp.append(art)

    with open('lineUp.txt', 'w') as f:
        for artista in sorted(lineUp):
            f.write(artista + '\n')
        
    print(len(lineUp))
    
    driver.close()
    driver.quit()

def comprobar_conexion(url):
    try:
        response = requests.get(url)
        # Verificar si la respuesta tiene un código de estado 2xx (éxito)
        response.raise_for_status()
        print(f"Conexión exitosa a {url}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"No se pudo conectar a {url}. Error: {e}")
        return False

if __name__ == '__main__':
    scrap()