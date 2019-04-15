#for reference, delete later:
#http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha=%22+startDate+%22&mod=deleg&fin=%22+endDate+%22&btnDo=Consultar'
#http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha=2010-01-01&mod=deleg&fin=2019-04-11&btnDo=Consultar

from bs4 import BeautifulSoup # need beautifulsoup for scraping
import requests, json # need these to access data on the internet and deal with structured data in my cache
from advanced_expiry_caching import Cache # use tool from the other file for caching
from datetime import date

FILENAME = 'cache.json'
program_cache = Cache(FILENAME)

def get_data(start_date, end_date):
    '''Gets data from the main page having been loaded for dates that you specify.'''
    url = 'http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha='+ start_date +'&mod=deleg&fin='+ end_date +'&btnDo=Consultar'
    data = program_cache.get(url)                                               #tries to get data from cache
    if not data:                                                                #if url with the given date periods isn't in the cache thn you request the data again
        data = requests.get(url).text
        program_cache.set(url, data, expire_in_days = 10)                       #place data into cache for later
    return data



#########################################################################################################################################
start_date = date(2019,3,1).strftime('%Y/%m/%d')
end_date = date(2019,3,31).strftime('%Y/%m/%d')
data=get_data(start_date, end_date)
soup = BeautifulSoup(data, "html.parser")
