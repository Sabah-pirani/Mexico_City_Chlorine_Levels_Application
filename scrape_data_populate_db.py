# -*- coding: utf-8 -*-
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

from bs4 import BeautifulSoup
import requests, json
from advanced_expiry_caching import Cache
from datetime import date, timedelta, datetime
from main_app import Delegacion, Calidad, session

######################### Scraping Functions ####################################
FILENAME = 'cache.json'
program_cache = Cache(FILENAME)

def scrape_pg(url):
    ''''''
    if program_cache.get(url):
        # print('inside try')
        data = program_cache.get(url)                                           # tries to get data from cache
        print('got fr cache')
    else:                                                                       # if url with the given date periods isn't in the cache then you request the data again
        # print('inside except')
        data = requests.get(url).text
        print('made request')
        program_cache.set(url, data, expire_in_days = 365)                      # place data into cache for later
        # print('done putting in cache')
    return data

def get_urls(data, urls_lst=[]):
    ''''''
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

############################## DB Functions #####################################

def add_delegacion_to_db(name):
    delegacion = Delegacion.query.filter_by(name=name).first()
    if delegacion:
        return delegacion
    else:
        delegacion = Delegacion(name=name)
        session.add(delegacion)
        session.commit()
    return delegacion

def add_calidad_to_db(date, neighborhood, street, num_samples, readings, average, num_no_cl, num_low_cl, num_rule_cl, num_excess_cl, url):
    calidad = Calidad.query.filter_by(date = date, street = street, average = average).first()
    if calidad:
        return calidad
    else:
        calidad = Calidad(date = date, neighborhood = neighborhood, street = street, num_samples = num_samples, readings = readings, average = average, num_no_cl = num_no_cl, num_low_cl = num_low_cl, num_rule_cl = num_rule_cl, num_excess_cl = num_excess_cl, url = url)
        session.add(calidad)
        session.commit()
    return calidad

######################## Scrape Data and Put into DB ############################

start_date = date(2019,1,1)
end_date = date(2019,1,31)
delta = end_date - start_date

for i in range(delta.days + 1):
    day = ((start_date + timedelta(days=i)).strftime('%Y/%m/%d'))
    print(day)
    url = 'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha='+ day +'&mod=deleg&fin='+ day +'&btnDo=Consultar'

    main_pg_html = scrape_pg(url)
    delegaciones = get_urls(main_pg_html)

    colonias = []
    for delegacion, url in delegaciones:
        add_delegacion_to_db(name=delegacion)
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


    for delegacion, colonia, cruce, url in cruces:
            data_pt = []
            tr_tags = get_tr_tags(url)
            for tr_tag in tr_tags :
                for pt in tr_tag.findChildren('td')[1:]:
                    if pt.text.strip()=='':
                        data_pt.append(0)
                    else:
                        data_pt.append(pt.text.strip())
                data_pt = []
                add_calidad_to_db (date = datetime.strptime(day,'%Y/%m/%d').date(), neighborhood = colonia, street = cruce, num_samples = int(data_pt[0]), readings = int(data_pt[1]), average = float(data_pt[2]), num_no_cl = int(data_pt[3]), num_low_cl = int(data_pt[4]), num_rule_cl = int(data_pt[5]), num_excess_cl = int(data_pt[6]), url = url)
