from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import streamlit as st

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

SLEEP = 10

# Acessando o site
url = 'https://tempo.inmet.gov.br/TabelaEstacoes/'
driver.get(url)
time.sleep(SLEEP)

# Clicando no menu
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div[1]/i').click()
time.sleep(SLEEP)

# Estado
estado = 'São Paulo'

# ESTACAO 
estacao = 'A701'

# Clicando no botao estacao automatica
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[2]/div[1]/button[1]').click()
time.sleep(SLEEP)

# Clicando na estacao
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[2]/div[3]/input').send_keys(estacao)
time.sleep(SLEEP)

# Clicando para gerar a tabela
driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div[2]/button').click()
time.sleep(10)

# Pegando a pagina
page = driver.page_source
soup = BeautifulSoup(page, 'lxml')
tabela = soup.find('table')
df = pd.read_html(str(tabela), decimal=',', thousands='.')[0]
df = pd.DataFrame(df.to_records())

colunas=['index','Date','Time','Tinst','Tmax','Tmin','URinst','URmax','URmin','PtOrvalhoinst','PtOrvalhomax','PtOrvalhmin','Pinst','Pmax','Pmin','Vveloc','Vdir','Vraj','Rad','Precipt']
for n in  range(0,len(df.keys())):
    
    df=df.rename(columns={df.keys()[n]: colunas[n]})

st.dataframe(df)