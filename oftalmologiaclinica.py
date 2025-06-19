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
link='https://www.oftalmologiaclinica.it/'

# %%
driver.get(link)

# %%
page=BeautifulSoup(driver.page_source,'html.parser')
alldoctors=page.find('div',id='wpsl-stores')
alltargets=alldoctors.find_all('li')

# %%
name=[]
specialist_title=[]
numtel=[]
email=[]
othercontacts=[]
adress=[]
url=[]


# %%
for a in alltargets:
    # Valores por defecto ─ si algo falta, quedará en None
    prename = None
    prespecialist = None
    phone = None
    mail = None
    other = None
    preadres =None
    preurl=None


    h2 = a.find('h2')
    if h2:
        prename = h2.get_text(strip=True)

    firsta=a.find('a')
    if firsta:
        preurl='https://www.oftalmologiaclinica.it'+a.find('a')['href']
    

    adresswrapper=a.find('div',class_='wpsl-store-name-wrapper')
    if adresswrapper:
        preadress=adresswrapper.get_text(strip=True)


    spec_div = a.find('div', class_='wpsl-specialization')
    if spec_div:
        prespecialist = spec_div.get_text(strip=True)


    contact_wrapper = a.find('div', class_='wpsl-contact-details-wrapper')
    if contact_wrapper:
        contacts = contact_wrapper.find_all('div', class_='wpsl-contact-details')

        if contacts:

            phone = contacts[0].get_text(strip=True).split(':', 1)[-1].strip()

            if len(contacts) > 1:
                mail = contacts[1].get_text(strip=True).split(':', 1)[-1].strip()

    
            if len(contacts) > 2:
                extra = [
                    c.get_text(strip=True).split(':', 1)[-1].strip()
                    for c in contacts[2:]
                ]
                other = ", ".join(extra)

    name.append(prename)
    specialist_title.append(prespecialist)
    numtel.append(phone)
    email.append(mail)
    othercontacts.append(other)
    adress.append(preadress)
    url.append(preurl)

# %%
sample=({
    'name':name,
    'specialist_title':specialist_title,
    'numtel':numtel,
    'email':email,
    'othercontacts':othercontacts,
    'adress':adress,
    'url':url

})

# %%
sample=pd.DataFrame(sample)

# %%
sample.to_csv('oftalmologiaclinica.csv',index=False)
sample.to_excel('oftalmologiaclinica.xlsx',index=False)


