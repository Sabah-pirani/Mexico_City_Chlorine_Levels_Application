import requests
import pandas as pd
from bs4 import BeautifulSoup
from numpy import *
from datetime import date
from datetime import timedelta
import os
import re

#code to import chlorine data from Mexico City SacMEX Database
#data  located at: http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/
#data organized by Delgacion-> Colonia (neighborhood)-> Cruise (street)
#   Delgacion (Delegation): http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha=2018-01-01&mod=deleg&fin=2019-03-01&btnDo=Consultar
#   Returns table of delagations with chlorine values
#       fecha=              (date)
#       mod=delg            (specify you want delegation)
#       fin=                (end date)
#
#   Colonia (neighborhood): http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?tipoConsulta=fecha&mod=col&deleg=1&fecha=2018-01-01&ndeleg=%C3%81lvaro%20Obreg%C3%B3n&fin=2018-03-01
#   Returns table of neighborhoods with chlorine values
#       tipoConsulta=fecha  (high level argument)
#       mod=col             (specify that you are asking about specific neighborhood)
#       deleg=              (delegation numbered, 1...18)
#       ndeleg=             (name of neighborhood, string)
#       fecha=              (start date)
#       fin=                (end date)

#   Cruise (street intersection):http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?tipoConsulta=fecha&mod=cruz&deleg=1&fecha=2018-01-01&ndeleg=%C3%81lvaro%20Obreg%C3%B3n&col=301022&ncol=BEJERO&fin=2018-03-01
#   Returns table of street intersections with chlorine values
#       tipoConsulta=fecha  (high level argument)
#       mod=cruz             (specify that you are asking about specific neighborhood)
#       deleg=              (delegation numbered, 1...15)
#       ndeleg=             (name of neighborhood, string)
#       col=                (numer of colonia,number)
#       ncol=               (name of colonia, string)

#how scraping will work: given a date range, grab each top level table and write to file, then descend into each link and create a foldr for each, repeat until you reach final level (Street)

#d1 = date(2013,1,1)
#d2 = date(2013,3,1)

#data starts roughly in 2010, with most not coming in

#delta = d2 - d1# timedelta

#for i in range(delta.days + 1):
#    print(d1 + timedelta(days=i)


def scrapeData(scrapeURL,rootDir):

    #webSrv = "http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha="+startDate+"&mod=deleg&fin="+endDate+"&btnDo=Consultar"
    #print (webSrv)

    response = requests.get(scrapeURL)
    while(response.status_code != 200):
        response = requests.get(scrapeURL)

    soup = BeautifulSoup(response.text, 'lxml') # Parse the HTML as a string
    table = soup.find_all('table')[0] # Grab the first table

    table = soup.find_all('table')[1]  # Grab the first table   (do you mean second?)

    new_table = []                     # array()#[][]#pd.DataFrame() # I know the size

    row_marker = 0
    for row in table.find_all('tr',{'class': "trLink"}):
        column_marker = 0
        columns = row.find_all('td')
        rowData = []
        links = row.find_all('a')
        if(len(links)>0):
            rowData.append(links[0].get('href'))
        else:
            rowData.append(0)

        for column in columns:
            rowData.append(column.get_text().strip())
            column_marker += 1
        #need to remove special charcters from site name
        rowData[1] = re.sub('[\\\\/*?:"<>|]','',rowData[1])
        #print(rowData)
        if(int(rowData[2].replace("","0"))) or int(rowData[3].replace("","0")):
            new_table.append(rowData)
            row_marker= row_marker + 1
        #print(rowData)


    #print(new_table)

    #wire to file
    header = "Date,Samples,Readings,Average,Zero,Low,Rule,Excess".strip()
    #print(header)
    if not os.path.exists(rootDir):
        os.makedirs(rootDir)

    for row in new_table:
        name = row[1]
        fileName = rootDir + name + ".csv"
        file = open(fileName,"a+")
        b = os.path.getsize(fileName)
        if b == 0:
            file.write(header+"\n")
        #print(fileName)
        vals = ",".join(row[2:])
        file.write(day+","+vals+"\n")
        file.close()

    #once done writing, descend donw the chain and get specific data
    for row in new_table:
        if(row[0]!=0):
            subUrl = "http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/" + row[0]
            #print(subUrl)
            subDir = rootDir + row[1] + "/"
            #print(subDir)
            scrapeData(subUrl,subDir)

#################################################################################################################################################
startDate = date(2018,1,1)
endDate = date(2018,2,28)

delta = endDate - startDate      # timedelta
for i in range(delta.days + 1):
    day = ((startDate + timedelta(days=i)).strftime('%Y/%m/%d'))
    print(day)
    scrapeURL = "http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/?fecha="+day+"&mod=deleg&fin="+day+"&btnDo=Consultar"
    scrapeData(scrapeURL,"./data/")

#getData("2018-03-01")
