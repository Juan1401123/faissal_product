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

# %%
link='https://annuairesante.ameli.fr/trouver-un-professionnel-de-sante/ophtalmologiste'

# %%
driver.get(link)

# %%
urlstoscrap=[]
soup=BeautifulSoup(driver.page_source,'html.parser')
allplaces=soup.find_all('li',class_='seo-departement')
for a in allplaces:
    href=a.find('a')['href']
    urlstoscrap.append('https://annuairesante.ameli.fr'+href)

# %%
secondariurls=[]
for e in urlstoscrap:
    driver.get(e)
    time.sleep(2)
    soup2=BeautifulSoup(driver.page_source,'html.parser')
    try:
      first=soup2.find('ul',class_='first')
      if first:
        links=first.find_all('li')
        if links:
           for i in links:
              temphtml=i.find('a')['href']
              if temphtml:
                 secondariurls.append(temphtml)
    except AttributeError:
       print('there is no element')
    try:
      first=soup2.find('ul',class_='second')
      if first:
        links=first.find_all('li')
        if links:
           for i in links:
              temphtml=i.find('a')['href']
              if temphtml:
                 secondariurls.append(temphtml)
    except AttributeError:
       print('there is no element')
    try:
      first=soup2.find('ul',class_='third')
      if first:
        links=first.find_all('li')
        if links:
           for i in links:
              temphtml=i.find('a')['href']
              if temphtml:
                 secondariurls.append(temphtml)
    except AttributeError:
       print('there is no element')

# %%
name=[]
specialist_title=[]
numtel=[]
adress=[]


# %%
for index,enlace in enumerate(secondariurls[916:]):
    numde=0
    driver.get('https://annuairesante.ameli.fr'+enlace)
    while numde==0:
      time.sleep(4)
      soup2=BeautifulSoup(driver.page_source,'html.parser')
      targets=soup2.find_all('div',class_='item-professionnel')
      print(index+916)
      for target in targets:
         try:
            prename=target.find('h2').text
            if prename:
               name.append(prename)
            else:
               name.append(None)
         except AttributeError:
            name.append(None)
         try:
            prespecialist_title=target.find('div',class_='item left specialite').text
            if prespecialist_title:
               specialist_title.append(prespecialist_title)
            else:
               specialist_title.append(None)
         except AttributeError:
            specialist_title.append(None)
         try:
            prenumtel=target.find('div',class_='item left tel').text
            if prenumtel:
               numtel.append(prenumtel)
            else:
               numtel.append(None)
         except AttributeError:
            try:
              prenumtel=target.find('div',class_='item right tel').text
              if prenumtel:
                  numtel.append(prenumtel)
              else:
                  numtel.append(None)
            except AttributeError:
                numtel.append(None)
         try:
            preadress=target.find('div',class_='item left adresse').text
            if preadress:
               adress.append(preadress)
            else:
               adress.append(None)
         except AttributeError:
            adress.append(None)
      if len(driver.find_elements(By.XPATH, '//img[@alt="Page suivante"]'))==0:
         numde=1
      else:
        next=driver.find_element(By.XPATH, '//img[@alt="Page suivante"]')
        time.sleep(1)
        next.click()
      

# %%
sample=({
    'name':name,
    'specialist_title':specialist_title,
    'numtel':numtel,
    'adress':adress

})

# %%
sample=pd.DataFrame(sample)

# %%
sample

# %%
sample.drop_duplicates(inplace=True)
sample.to_csv('annuairesante.csv',index=False)
sample.to_excel('annuairesante.xlsx',index=False)


