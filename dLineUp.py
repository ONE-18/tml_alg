from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def descargarLineUp(driver): 
    pass

def scrap():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.tomorrowland.com/en/festival/line-up?weekend=W1&day=19/07/2024')
    
    wait = WebDriverWait(driver, 10)
    
    lineUp = []
    
    for i in range(2):      # iterar entre los 2 fines de semana
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//tml-lineup')))
        
        lineUp.append(descargarLineUp(driver))

        for j in range(3):  # iterar entre los 3 días de cada fin de semana
            botones = driver.find_elements(By.XPATH,'//tml-lineup/div')
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/tml-lineup//div/div[2]/button[2]'))).click()
        
            lineUp.append(descargarLineUp(driver))
        
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/tml-lineup//div/div[1]/button[2]'))).click()
        
if __name__ == '__main__':
    scrap()