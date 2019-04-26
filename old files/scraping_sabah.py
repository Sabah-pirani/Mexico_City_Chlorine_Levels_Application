# -*- coding: utf-8 -*-
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

from bs4 import BeautifulSoup
import requests, json
from advanced_expiry_caching import Cache
from datetime import date, timedelta
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this
from db_table_models import Delegacion, Calidad
import sys

#################### Flask Application Configurations ###########################

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sacmex_cdmx_data.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
session = db.session

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

def add_calidad_to_db(date, neighborhood, street, num_samples, readings, average, percent_none,percent_low, percent_rule, percent_excess, url):
    calidad = Calidad.query.filter_by(**args).first()
    if calidad:
        return calidad
    else:
        calidad = Calidad(date = date, neighborhood = neighborhood, street = street, num_samples = num_samples, readings = readings, average = average, percent_none = percent_none, percent_low = percent_low, percent_rule = percent_rule, percent_excess = percent_excess)
        session.add(calidad)
        session.commit()
    return calidad

######################### Scraping Functions ####################################
FILENAME = 'cache.json'
program_cache = Cache(FILENAME)

def scrape_pg(url):
    '''Attempts to find data in cache, if unable requests data from webpage and saves it in the cache. Returns scraped data as text.'''
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
########################### Main code ###########################################

start_date = date(2019,3,1)
end_date = date(2019,3,1)
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
                    data_pt.append(pt.text.strip())
                add_calidad_to_db(day, colonia, cruce, data_pt[0], data_pt[1], data_pt[2], data_pt[3], data_pt[4], data_pt[5], data_pt[6], url)
                data_pt = []










    # all_data=[]
    # for delegacion, colonia, cruce, url in cruces:
    #         data_pt = []
    #         tr_tags = get_tr_tags(url)
    #         for tr_tag in tr_tags :
    #             data_pt.append(day)
    #             data_pt.append(delegacion)
    #             data_pt.append(colonia)
    #             data_pt.append(cruce)
    #             for pt in tr_tag.findChildren('td')[1:]:
    #                 data_pt.append(pt.text.strip())
    #             data_pt.append(url)
    #             all_data.append(data_pt)
    #             data_pt = []
