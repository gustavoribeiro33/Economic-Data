import requests
from bs4 import BeautifulSoup
import json

proxies={'https':'//10.2.6.250:3128'}

#Nasdaq

with open('nasdaq.json') as file:
    nasdaqbase = json.load(file)

with open('nasdaqmatch.json', 'r') as file:
    assetclass = json.load(file)

#B3
with open('b3.json') as file:
    b3base = json.load(file)

#BCB

bcbbase = {}

with open('bcb.json') as file:
    read = json.load(file)
    for i in range(read.__len__()):
        serie = read[i].get('1')
        nome = read[i].get('Taxa de câmbio - Livre - Dólar americano (venda) - diário')
        bcbbase.update({serie:nome})

#FRED

fredbase = {}

with open('fred.json') as file:
    read = json.load(file)
    listed = read['seriess']
    for i in range(listed.__len__()):
        serie = listed[i].get('id')
        nome = listed[i].get('title')
        fredbase.update({serie:nome})

#Ipea

ipeabase = {}

with open('ipea.json') as file:
    read = json.load(file)
    series = read['data']
    
    for serie in series:
        code = serie.get('CODE')
        name = serie.get('NAME')
        ipeabase.update({code:name})