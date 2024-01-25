from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup

def generar_url():
    url = 'https://www.tomorrowland.com/en/festival/line-up?weekend=W1&day=19/07/2024'
    
    # url_base = 'https://www.tomorrowland.com/en/festival/line-up?weekend=W1&day='
    url_base = url[:]   # TODO revisar

    fecha = datetime.strptime('19/07/2024', '%d/%m/%Y')

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


# def descargarLineUp(driver): 
#     pass

# def scrap():
#     options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')
    
#     driver = webdriver.Chrome(options=options)
#     driver.get('https://www.tomorrowland.com/en/festival/line-up?weekend=W1&day=19/07/2024')
    
#     wait = WebDriverWait(driver, 10)
    
#     lineUp = []
    
#     for i in range(2):      # iterar entre los 2 fines de semana
        
#         wait.until(EC.presence_of_element_located((By.XPATH, '//tml-lineup')))
        
#         lineUp.append(descargarLineUp(driver))

#         for j in range(3):  # iterar entre los 3 días de cada fin de semana
#             botones = driver.find_elements(By.XPATH,'//*[@id="lineup"]/')
#             wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/tml-lineup//div/div[2]/button[2]'))).click()
        
#             lineUp.append(descargarLineUp(driver))
        
#         wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/tml-lineup//div/div[1]/button[2]'))).click()

if __name__ == '__main__':
    
    generador = generar_url()
    for url in generador:
        with open('html.txt', 'w') as file:
            file.write(descargar_html(url))
    # html = descargar_html(url)