# -*- coding: utf-8 -*-
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

#Imports from Files:
from advanced_expiry_caching import Cache
from main_app import Delegacion, Calidad, Fecha, session

#Imports from libraries:
from bs4 import BeautifulSoup
import requests, json
from datetime import date, timedelta, datetime
import time
import unidecode

######################### Scraping Functions ####################################
FILENAME = 'cache.json'
program_cache = Cache(FILENAME)

def scrape_pg(url):
    ''''''
    if program_cache.get(url):
        # print('inside try')
        data = program_cache.get(url)                                           # tries to get data from cache
        # print('got fr cache')
    else:                                                                       # if url with the given date periods isn't in the cache then you request the data again
        # print('inside except')
        data = requests.get(url).text
        # print('made request')
        program_cache.set(url, data, expire_in_days = 365)                      # place data into cache for later
        # print('done putting in cache')
    return data

def get_urls(data, urls_lst=[]):
    ''''''
    soup = BeautifulSoup(data, "html.parser")                                   #
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
    ''''''
    data = scrape_pg(url)
    soup = BeautifulSoup(data, "html.parser")
    return soup.findChildren('tr', {"class": "trLink"})

############################## DB Functions #####################################

def get_or_create_delegacion_db(name):
    ''''''
    accents_removed_delegacion = unidecode.unidecode(name)
    delegacion = Delegacion.query.filter_by(name=accents_removed_delegacion).first()
    if delegacion:
        return delegacion
    else:
        delegacion = Delegacion(name=accents_removed_delegacion)
        session.add(delegacion)
    return delegacion

def add_to_calidad_db(date, neighborhood, street, num_samples, readings, average, num_no_cl, num_low_cl, num_rule_cl, num_excess_cl, url, delegacion):
    ''''''
    accents_removed_delegacion = unidecode.unidecode(delegacion)
    accents_removed_neighborhood = unidecode.unidecode(neighborhood)
    accents_removed_street = unidecode.unidecode(street)
    delegacion = get_or_create_delegacion_db(accents_removed_delegacion)
    calidad = Calidad(date = date, neighborhood = accents_removed_neighborhood, street = accents_removed_street, num_samples = num_samples, readings = readings, average = average, num_no_cl = num_no_cl, num_low_cl = num_low_cl, num_rule_cl = num_rule_cl, num_excess_cl = num_excess_cl, url = url, delegacion = delegacion)
    session.add(calidad)
    return None

def add_to_date_db(date):
    ''''''
    fecha = Fecha.query.filter_by(date = date).first()
    if not fecha:
        date = Fecha(date = date)
        session.add(date)
    else:
        pass
    return None

######################## Scrape Data and Put into DB ############################
start_time = time.time()

start_date = date(2019,4,1)
end_date = date(2019,4,4)
delta = end_date - start_date

for i in range(delta.days + 1):

    day = ((start_date + timedelta(days=i)).strftime('%Y/%m/%d'))
    dt_date = datetime.strptime(day,'%Y/%m/%d').date()
    print('hello',day)

    url = 'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha='+ day +'&mod=deleg&fin='+ day +'&btnDo=Consultar'

    if Fecha.query.filter_by(date=dt_date).first():
        pass

    add_to_date_db(date = dt_date)

    main_pg_html = scrape_pg(url)
    delegaciones = get_urls(main_pg_html)

    colonias = []
    for delegacion, url in delegaciones:
        get_or_create_delegacion_db(name=delegacion)
        tr_tags = get_tr_tags(url)
        for tr_tag in tr_tags:
            tr_tag.findChild('a', {"class": "cargaCont"}, href=True)
            a = tr_tag.findChild('a', {"class": "cargaCont"}, href=True)
            url = 'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua'+ a['href']
            colonia = (a.text.strip())
            colonias.append([delegacion, colonia, url])

    cruces = []
    for delegacion, colonia, url in colonias:
            tr_tags = get_tr_tags(url)
            for tr_tag in tr_tags:
                cruce = tr_tag.findChild('td', {"class": "linkDel"}).text.strip()
                data_pt = []
                for pt in tr_tag.findChildren('td')[1:]:
                    if pt.text.strip()=='':
                        data_pt.append(0)
                    else:
                        data_pt.append(pt.text.strip())

                add_to_calidad_db (date = dt_date, neighborhood = colonia, street = cruce, num_samples = int(data_pt[0]), readings = int(data_pt[1]), average = float(data_pt[2]), num_no_cl = int(data_pt[3]), num_low_cl = int(data_pt[4]), num_rule_cl = int(data_pt[5]), num_excess_cl = int(data_pt[6]), url = url , delegacion = delegacion)


    session.commit()

print("--- %s seconds ---" % (time.time() - start_time))
