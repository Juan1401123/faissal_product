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


link='https://str.optical.org/'


driver.get(link)

inputspecialty=driver.find_element(By.CSS_SELECTOR,'#Registrant-Register-input > option:nth-child(2)')
time.sleep(1)

inputspecialty.click()

clicksearch=driver.find_element(By.CSS_SELECTOR,'#searchform > div.card-footer > button.btn.btn-primary.float-right.mt-3')
time.sleep(1)
clicksearch.click()
time.sleep(3)

data1=[]
data2=[]
data3=[]
data4=[]
urls=[]



soup1 = BeautifulSoup(driver.page_source, 'html.parser')
prepage = soup1.find('p', class_='d-block text-right mt-4')
if not prepage:
    raise ValueError("No se encontró el texto de número de páginas.")

maxpage = int(prepage.text.strip().split()[-1])

for numpage in range(1, maxpage + 1):
                    try:
                        print(numpage)
                        inputpag = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, 'goToPageInput'))
                        )
                        inputpag.clear()
                        time.sleep(.5)
                        inputpag.send_keys(numpage)
                        time.sleep(.5)

                        searchbutton = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search-results > div.card-body > div:nth-child(3) > div.col-md-4 > div > div > button'))
                        )
                        searchbutton.click()
                        time.sleep(1)

       
                        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                        alltargets = soup2.find_all('li', class_='media mb-3 border-bottom pb-3')

                        for target in alltargets:
                            try:
                                predata1 = target.find('strong')
                                data1.append(predata1.text if predata1 else None)
                            except:
                                data1.append(None)
                            
                            
                            try:
                                predata2 = target.find('div', class_='media-body')
                                preurl=target.find('a', class_='btn btn-primary')['href'] if predata2 else None
                                if preurl:
                                    preurl = 'https://str.optical.org' + preurl
                                    urls.append(preurl)
                                if predata2:
                                    lines = predata2.text.strip().split('\n')
                                    if lines:
                                        data2.append(lines[len(lines)-1].strip())
                                    else:
                                        data2.append(None)
                                else:
                                    data2.append(None)
                            except:
                                data2.append(None)
                            
                            
                            try:
                                predata3 = target.find('div', class_='media-body')
                                if predata3:
                                    lines = predata3.text.strip().split('\n')
                                    if lines:
                                        data3.append(lines[len(lines)-2].strip())
                                    else:
                                        data3.append(None)
                                else:
                                    data3.append(None)
                            except:
                                data3.append(None)
                            try:
                                predata4 = target.find('div', class_='media-body')
                                if predata4:
                                    lines = predata4.text.strip().split('\n')
                                    if lines:
                                        data4.append(lines[len(lines)-3].strip())
                                    else:
                                        data4.append(None)
                                else:
                                    data4.append(None)
                            except:
                                data4.append(None)
                    except Exception as e:
                        print(f"[!] Error en paginación página {numpage}: {e}")
                        continue


sample=({'Name':data1,
         'Adress':data2,
         'Speciality':data3,
         'Register_as':data4,
            'Url':urls
         

})


sample=pd.DataFrame(sample)

sample.drop_duplicates(inplace=True)

sample.reset_index(drop=True, inplace=True)


sample['Personal Adress']=None
sample['Town']=None


for index,e in enumerate(sample['Personal Adress']):
    

    if e is None:
            link = sample['Url'][index]
            driver.get(link)
            time.sleep(1)
            soup3 = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                preTown = soup3.find('div', attrs={'aria-label': 'Town', 'class': 'media-body'}).text.replace('\n', ' ').strip()
                if preTown:
                    sample['Town'][index] = preTown
        
            except AttributeError:
                print(f"[!] Error al obtener la ciudad personal para {e}: {e}")
            try:
                prePersonalAdress = soup3.find('div', attrs={'aria-label': 'Practice addresses', 'class': 'media-body'}).text.replace('\n', ' ').strip()
                if prePersonalAdress:
                    sample['Personal Adress'][index] = prePersonalAdress
            except AttributeError:
                print(f"[!] Error al obtener la dirección personal para {e}: {e}")




sample.to_csv('stroptical_2.csv',index=False)
sample.to_excel('stroptical_2.xlsx',index=False)