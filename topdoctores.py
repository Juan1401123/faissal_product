# %%
import re
import time
from colorama import Fore
import openpyxl
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import random
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import math

# %%
options = Options()

options.add_argument('--disable-application-cache')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-cookies")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument('--disable-gpu')
# options.add_argument("--headless")  
# options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--ignore-urlfetcher-cert-requests')
options.add_argument('--no-first-run')
options.add_argument("--disable-popup-blocking") 


driver = webdriver.Chrome(options=options)

# %% [markdown]
# https://www.topdoctors.es/oftalmologia/

# %%
driver.get('https://www.topdoctors.es/oftalmologia/')

# %%
name=[]
numtel=[]
expert=[]
specialist_title=[]
hospitals=[]
price=[]
ranking=[]
opinions=[]
urls=[]

# %%
num_next=0
while num_next==0:
    numerostel=[]
    time.sleep(1)
    driver.execute_script(f"window.scrollBy(0, {4500});")
    time.sleep(2)
    WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-id="provider"]'))
)
    
    targets=driver.find_elements(By.CSS_SELECTOR, 'li[data-id="provider"]')
    for target in targets:
        htmltarget=target.get_attribute('outerHTML')
        soup=BeautifulSoup(htmltarget,'html.parser')
        try:
            prename=target.find_element(By.XPATH, './/h2').text
            if name:
                name.append(prename)
            else:
                name.append(None)
        except NoSuchElementException:
            name.append(None)
        try:
            anteurl=soup.find('h2')
            preurl=anteurl.find('a')['href']
            if preurl:
                urls.append('https://www.topdoctors.es'+preurl)
            else:
                urls.append(None)
        except NoSuchElementException:
            urls.append(None)
        try:
            prespecialist_title=target.find_element(By.XPATH, '//*[starts-with(@class, "specialist-title")]').text
            if prespecialist_title:
               specialist_title.append(prespecialist_title)
            else:
                specialist_title.append(None)
        except NoSuchElementException:
            specialist_title.append(None)
        
        try:
            preexperts=soup.find('div',class_='profile-nowrap clamped skills-list') #skills is-contents is-boxed is-results-ul
            eachexperts=preexperts.find_all('li')[1:]
            if len(eachexperts)>1:
                arrexperts=[]
                for b in eachexperts:
                    arrexperts.append(b.text)
                expert.append(arrexperts)
            else:
              expert.append(None)      
        except AttributeError:
            try:
                preexperts=soup.find('ul',class_='skills is-contents is-boxed is-results-ul') #skills is-contents is-boxed is-results-ul
                eachexperts=preexperts.find_all('li')[1:]
                if len(eachexperts)>1:
                    arrexperts=[]
                    for b in eachexperts:
                        arrexperts.append(b.text)
                    expert.append(arrexperts)
                else:
                  expert.append(None)      
              
            except AttributeError:
                expert.append(None)  
        try:
            preprice=soup.find('span', class_=re.compile('^selected-product__price')).text.replace('\xa0','')
            if preprice:
                price.append(preprice)
            else:
                price.append(None)
        except AttributeError:
            price.append(None)
        try:
            preranking=soup.find('span', class_='text-average-rating').text.replace(' | \xa0 ','')
            if preranking:
                ranking.append(preranking)
            else:
                ranking.append(None)
        except AttributeError:
            ranking.append(None)
        try:
            preopinions=soup.find('p', class_='flex-center gap-quarter').text.replace('\xa0 ','')
            if preopinions:
                opinions.append(preopinions)
            else:
                opinions.append(None)
        except AttributeError:
            opinions.append(None)
        try:
            buttontell = target.find_element(By.XPATH, './/button[starts-with(@class, "is-primary action-btn")]')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(buttontell)).click()
    
                # Esperar a que se muestre el contenido después del click (ajusta si necesitas otra condición)
            WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, .popup, .info-visible"))
                )
            
            souptell=BeautifulSoup(driver.page_source,'html.parser')
            main=souptell.find('main',class_='modal-content__body')       
            try:
             prenum=main.find('a', attrs={'dir': 'ltr'}).text
             if prenum:
                 numtel.append(prenum)
             else:
                 numtel.append(None)
            except AttributeError:
                  numtel.append(None)  
            try:
                prehospital=main.find('div',class_='selected-item').text
                if prehospital:
                    hospitals.append(prehospital)
                else:
                    hospitals.append(None)
            except AttributeError:
                hospitals.append(None)
    
            driver.execute_script("document.elementFromPoint(200, 300).click();")
        except NoSuchElementException:
            hospitals.append(None)
            numtel.append(None)  
    driver.execute_script(f"window.scrollBy(0, {4500});")
    time.sleep(2)
    next_buttons = driver.find_elements(By.CLASS_NAME, 'pagination-next')
    if not next_buttons:
        num_next = 1
    else:
        try:
            next_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-next'))
            )
            next_btn.click()

            # Esperar a que cambie la página (aquí usamos de nuevo el cargado de los providers)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-id="provider"]'))
            )
        except Exception as e:
            print(f"❌ Error al hacer clic en 'Siguiente': {e}")
            num_next = 1

# %%




# %%
sample=({
    'name':name,
    'hospitals':hospitals,
    'experts':expert,
    'numtel':numtel,
    'specialist_title':specialist_title,
    'ranking':ranking,
    'opinions':opinions,
    'price':price,
    'urls':urls

})

# %%
pd.DataFrame(sample)

# %%
sample=pd.DataFrame(sample)

# %%
sample.to_csv('topdoctors.csv',index=False)
sample.to_excel('topdoctors.xlsx',index=False)


