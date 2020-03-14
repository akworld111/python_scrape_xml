# Built by Abdul 2020/03/01

import requests
from xml.etree import ElementTree
import logging

import csv
import codecs
from bs4 import BeautifulSoup

def write_data(writer, url, code,acc  ):
    writer.writerow({'url': url, 'cik_code': code, 'accurate':acc})

def parse_cik_code(writer, url):
  response = requests.get(url)
  root = ElementTree.fromstring(response.content)
  code = ''
  accurate= ''
  is_havedata = False

  if 'AccruedEnvironmentalLossContingenciesCurrent' in response.text:
    soup = BeautifulSoup(response.content, 'lxml')
    tag_list = soup.find_all()
    for tag in tag_list:
      if tag.name == 'us-gaap:accruedenvironmentallosscontingenciescurrent':
        is_havedata = True
        accurate += ", " + tag.text
        logging.info("AccruedEnvironmentalLossContingenciesCurrent: " + tag.text)
    

  for level1 in root.findall('{www.xbrl.org/2003/'):
    for level2 in level1.find('{www.xbrl.org/2003}entity'):       
        if level2 is not None:
          try:
            cikCode =  level2.text.strip()
          except:
            logging.error("level2 error")
          if cikCode: 
            code = cikCode
            is_havedata = True
            #logging.info("level2: " + level2.text)

  if is_havedata == True:
    write_data(writer, url, code, accurate)    

with open('url list.csv',) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=' ')
    with open("output.csv", mode='w') as csv_file:
      fieldnames = ['url', 'cik_code', 'accurate']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      writer.writeheader()  
      for row in readCSV:
        #import pdb ;pdb.set_trace()
        if row[0].endswith(".xml"):
          print("parsing data:" + row[0])
          parse_cik_code(writer,row[0])


