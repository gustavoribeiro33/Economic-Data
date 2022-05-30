import requests
import pandas as pd
import ipeadatapy as ipea
import serieslist
import datetime
import dateutil.parser

# If you are using a proxy, enter your proxy address on the variable bellow:
proxies = {''}

# In order do use Federal Reserve Economic Data, you need a API key, you can get one in the FRED API website, once you have obtained it, enter it on the variable bellow:
fredapikey = ''


def NASDAQ(assetname, startdate, enddate):
    # DataFormat Conversion
    startparse = dateutil.parser.parse(startdate)
    startdate = startparse.strftime('%Y-%m-%d')

    endparse = dateutil.parser.parse(enddate)
    enddate = endparse.strftime('%Y-%m-%d')

    # Scrape
    assetclass = serieslist.assetclass.get(assetname)
    url = f'https://api.nasdaq.com/api/quote/{assetname}/historical?assetclass={assetclass}&fromdate={startdate}&limit=9999&todate={enddate}'
    header = {'User-Agent': 'foo'}
    r = requests.get(url, proxies=proxies, stream=True, headers=header)
    p = r.json()['data']
    q = p['tradesTable']
    r = q['rows']
    df = pd.DataFrame.from_records(r)
    df.to_excel(f'NASDAQ.xlsx')


def BCB(assetname, startdate, enddate):
    # DataFormat Conversion
    startparse = dateutil.parser.parse(startdate)
    startdate = startparse.strftime('%d/%m/%Y')

    endparse = dateutil.parser.parse(enddate)
    enddate = endparse.strftime('%d/%m/%Y')

    # Scrape
    link = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{assetname}/dados?formato=json&dataInicial={startdate}&dataFinal={enddate}'
    r = requests.get(link, proxies=proxies)
    p = r.json()
    df = pd.DataFrame.from_dict(p)
    df.to_excel(f'{assetname}.xlsx', index=False)


def FRED(assetname, startdate, enddate):

    series_id = assetname

    # DataFormat Conversion
    startparse = dateutil.parser.parse(startdate)
    start = startparse.strftime('%Y-%m-%d')

    endparse = dateutil.parser.parse(enddate)
    end = endparse.strftime('%Y-%m-%d')

    # Scrape

    api_key = fredapikey
    api_baseurl = 'https://api.stlouisfed.org/fred/'
    api_endurl = f'/series/observations?series_id={series_id}'
    file_type = '&file_type=json'
    ob_start = f'&observation_start={start}'
    ob_end = f'&observation_end={end}'

    r = requests.get(
        f'{api_baseurl}{api_endurl}&api_key={api_key}{file_type}{ob_start}{ob_end}', proxies=proxies, stream=True)
    p = r.json()['observations']
    df = pd.DataFrame.from_dict(p)
    df.drop(df.columns[[0, 1]], axis=1, inplace=True)
    df.to_excel('FRED.xlsx')


def B3(assetname, datainicial, datafinal):
    if assetname.__len__() > 6:
        series = assetname[4:]
    else:
        series = assetname

    print(series)
    url = f'https://cotacao.b3.com.br/mds/api/v1/DerivativeQuotation/{series}'
    r = requests.get(url, proxies=proxies)
    text = r.json()['Scty']
    sdata = []
    staxa = []

    for entry in text:
        data = entry.get('asset').get('AsstSummry').get('mtrtyCode')
        taxa = entry.get('SctyQtn').get('prvsDayAdjstmntPric')
        sdata.append(data)
        staxa.append(taxa)

    dados = {'Data': sdata, 'Taxa': staxa}
    df = pd.DataFrame.from_dict(dados)
    df.to_excel(f'{assetname}.xlsx')


def IPEA(assetname, datainicial, datafinal):
    # DataFormat Conversion
    startparse = dateutil.parser.parse(startdate)
    startdate = startparse.strftime('%d-%m-%Y')

    endparse = dateutil.parser.parse(startdate)
    enddate = endparse.strftime('%d-%m-%Y')

    # Scrape
    series = ipea.timeseries(assetname, yearGreaterThan=datainicial[-4:])
    series.to_excel(f"{assetname}.xlsx")
