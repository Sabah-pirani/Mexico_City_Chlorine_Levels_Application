#'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua'

# -*- coding: utf-8 -*-
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

from bs4 import BeautifulSoup
import requests, json
from advanced_expiry_caching import Cache
from datetime import date, timedelta
import sys
from db_and_flask import Delegacion, Calidad

FILENAME = 'cache.json'
program_cache = Cache(FILENAME)

def scrape_pg(url):
    '''Attempts to find data in cache, if unable requests data from webpage and saves it in the cache. Returns scraped data as text.'''
    if program_cache.get(url):
        # print('inside try')
        data = program_cache.get(url)                                           # tries to get data from cache
        print('complete try')
    else:                                                                       # if url with the given date periods isn't in the cache then you request the data again
        # print('inside except')
        data = requests.get(url).text
        print('made request')
        program_cache.set(url, data, expire_in_days = 10)                       # place data into cache for later
        # print('done putting in cache')
    return data

def get_urls(data, urls_lst=[]):
    '''Takes scraped data from a webpage, finds the tr tags with class 'trLink', parses the url and url text and returns a list of 2 element lists. the first element is the url text and the second element is the url.'''
    soup = BeautifulSoup(data, "html.parser")
    tr_tags=soup.findChildren('tr', {"class": "trLink"})
    for tr_tag in tr_tags:
        if tr_tag.findChild('a', {"class": "cargaCont"}, href=True):
            a = tr_tag.findChild('a', {"class": "cargaCont"}, href=True)
            url = 'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua'+ a['href']
            url_text = (a.text.strip())
        else:
            pass
        urls_lst.append([url_text, url])
    return urls_lst

def get_tr_tags(url):
    data = scrape_pg(url)
    soup = BeautifulSoup(data, "html.parser")
    return soup.findChildren('tr', {"class": "trLink"})

#########################################################################################################################################

start_date = date(2019,3,1)
end_date = date(2019,3,1)
delta = end_date - start_date

for i in range(delta.days + 1):
    day = ((start_date + timedelta(days=i)).strftime('%Y/%m/%d'))
    print(day)
    url = 'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha='+ day +'&mod=deleg&fin='+ day +'&btnDo=Consultar'

    # main_pg_html = scrape_pg('https://www.nps.gov/index.htm')
    main_pg_html = scrape_pg(url)
    delegaciones = get_urls(main_pg_html)

    colonias = []
    for delegacion, url in delegaciones:
        tr_tags = get_tr_tags(url)
        for tr_tag in tr_tags:
            if tr_tag.findChild('a', {"class": "cargaCont"}, href=True):
                a = tr_tag.findChild('a', {"class": "cargaCont"}, href=True)
                url = 'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua'+ a['href']
                colonia = (a.text.strip())
            else:
                pass
            colonias.append([delegacion, colonia, url])

    cruces = []
    for delegacion, colonia, url in colonias:
            tr_tags = get_tr_tags(url)
            for tr_tag in tr_tags:
                td = tr_tag.findChild('td', {"class": "linkDel"})
                cruce = (td.text.strip())
                cruces.append([delegacion, colonia, cruce, url])

    all_data=[]
    for delegacion, colonia, cruce, url in cruces:
            data_pt = []
            tr_tags = get_tr_tags(url)
            for tr_tag in tr_tags :
                data_pt.append(day)
                data_pt.append(delegacion)
                data_pt.append(colonia)
                data_pt.append(cruce)
                for pt in tr_tag.findChildren('td')[1:]:
                    data_pt.append(pt.text.strip())
                data_pt.append(url)
                all_data.append(data_pt)
                data_pt = []

for data in all_data:
    print(len(data))
    print('----------------')
