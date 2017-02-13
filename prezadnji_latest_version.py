from bs4 import BeautifulSoup
import sys
import requests
from lxml import html
import urllib2
import csv
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import itertools


def main(filePath):
    print(filePath)
    listOfPrograms = readFile(filePath)
    # print programs from list to console
    print("List of all programs from file: {0}".format(listOfPrograms))

    all_urls = []
    for program in listOfPrograms:
        url = createRequestURL(program)
        all_urls.append(url)

 
    outfile = open('outfile.csv', 'wb')
    headers = ('KANAL', 'SATELIT' ,'POLARIZACIJA', 'STUPNJEVI','FREKVENCIJA',  'SID', 'PAKET', 'DVB', 'MODULACIJA', 'SYMBOL_RATE', 'FEC', 'TID' , 'ONID', 'ENKRIPCIJA', 'TIP')
    writer1 = csv.writer(outfile, delimiter=';')

    writer1.writerow(headers)
 
    for url in all_urls:
        tables = getAllTables(url)
        #headers = tables[0].keys()
        headers = ('KANAL', 'SATELIT' ,'POLARIZACIJA', 'STUPNJEVI','FREKVENCIJA',  'SID', 'PAKET', 'DVB', 'MODULACIJA', 'SYMBOL_RATE', 'FEC', 'TID' , 'ONID', 'ENKRIPCIJA', 'TIP')
        
        for data in tables:

            line = []
            for filed in headers:

                line.append(data[filed])

            for item in line:

                if item == 'Name':
                    line[:]=[]

            if line != []:        
                   
                writer1.writerow(line)     
    outfile.close()
  

def readFile(pathToFile):
    listOfPrograms = []

    with open(pathToFile) as f:
        for line in f.readlines():
            line = line.strip()
            if line != "":
                listOfPrograms.append(line)

    return listOfPrograms

def createRequestURL(TVprogram):

    url = "http://en.kingofsat.net/find.php?question={0}".format(TVprogram)

    return url



def getAllTables(requestURL):

    tablice_all = []
    response = requests.get(requestURL)
    html_doc = response.content
    soup = BeautifulSoup(html_doc, 'lxml')
    all_tables = soup.findAll("table", { "class" :['frq', 'fl'] })
    div1 = soup.find('table', class_="frq")

    for tablice in all_tables:            
        tablice_all.append(tablice)    


    lista = []

    for tabs in tablice_all:   
        if tabs.find('tr', bgcolor="#D2D2D2"):
            coli = tabs.findAll('td')
            col1 = tabs.findAll('a')
       
            sateliti = col1[1].string
            freq = coli[2].string
            pol = coli[3].string
            dvb_type = coli[6].string
            qpsk = coli[7].string
            params1 = col1[4].string
            params2 = col1[5].string
            ni = coli[10].string
            ti = coli[11].string
            stupnjevi = col1[0].string

       
        if tabs.find("td", { "class" : "s" }):
            table_data = tabs('tr')
            for row in table_data:
                col = row.findAll('td')
                td_radio = row.findAll('img')
                radio_osobine = "/radio.gif" 
                data_osobine = "/data.gif"

                for non_tv in td_radio:
                    

                    if non_tv['src'] == radio_osobine:
                        

                        ime_kanal = col[2].text +" "+'(radio)'
                        package = col[3].text     
                        sid = col[5].text
                        fta = col[4].text
                        tip = "radio"
                      
                        
                        dictionary = {"TIP" : tip,'FEC' : params1, 'SID' : sid,'PAKET' : package, 'SATELIT' : sateliti,'STUPNJEVI' : stupnjevi,  'FREKVENCIJA' : freq, 'POLARIZACIJA' : pol, 'DVB' : dvb_type, 'MODULACIJA' : qpsk, 'KANAL' : ime_kanal, 'SYMBOL_RATE' : "\"%s\""%params2, 'ONID' : ni, 'TID' : ti, 'ENKRIPCIJA' : fta}
                        lista.append(dictionary)


                    elif non_tv['src'] == data_osobine:

                        ime_kanal = col[2].text +" "+'(data)'
                        package = col[3].text     
                        sid = col[5].text
                        fta = col[4].text
                        tip ="data"
                       

                        
                        dictionary = {"TIP" : tip,'FEC' : params1, 'SID' : sid,'PAKET' : package, 'SATELIT' : sateliti,'STUPNJEVI' : stupnjevi,  'FREKVENCIJA' : freq, 'POLARIZACIJA' : pol, 'DVB' : dvb_type, 'MODULACIJA' : qpsk, 'KANAL' : ime_kanal, 'SYMBOL_RATE' : "\"%s\""%params2, 'ONID' : ni, 'TID' : ti, 'ENKRIPCIJA' : fta}
                        lista.append(dictionary)
                        

                    else:            

                        
                        ime_kanal = col[2].text
                        package = col[5].text     
                        sid = col[7].text
                        fta = col[6].text
                        tip = "tv"
                       
                        
                        dictionary = {"TIP" : tip,'FEC' : params1, 'SID' : sid,'PAKET' : package, 'SATELIT' : sateliti,'STUPNJEVI' : stupnjevi,  'FREKVENCIJA' : freq, 'POLARIZACIJA' : pol, 'DVB' : dvb_type, 'MODULACIJA' : qpsk, 'KANAL' : ime_kanal, 'SYMBOL_RATE' : "\"%s\""%params2, 'ONID' : ni, 'TID' : ti, 'ENKRIPCIJA' : fta}
                        lista.append(dictionary)

    novo_uniq_lista = [dict(y) for y in set(tuple(x.items()) for x in lista)]
    return novo_uniq_lista

if __name__ == "__main__":
    filePath = sys.argv[1]
    if filePath:
        main(filePath)
    else:
        print('Too much arguments passed')
