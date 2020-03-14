# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
from w3lib.html import replace_escape_chars
import re
from enum import Enum

def removeMoneySymbol(value):
    """remove money symbol
    
    Arguments:
        value {string} -- input value
    
    Returns:
        string -- output value
    """
    trim = re.compile(r'[^\d.,]+')
    value = trim.sub('', value)
    value = value.replace(",",".")
    return value

def getQuantity(value):
    """Get quantity in a string
    
    Arguments:
        value {string} -- input string
    
    Returns:
        string -- quantity
    """
    if value:
        value = str(value)
        value = re.findall(r'(\d+)', value, re.MULTILINE)
        if value:
            value = value[0]
            value = convertToInt(value)
        else:
            value = 0
    
    return value

def getMoney(value):
    """get money from a string
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- money
    """
    if value is not None:
        trim = re.compile(r'[^\d.,]+')
        value = trim.sub('', value)
        value = value.replace(",",".")
        return convertToFloat(value)
    else:
        return value

def convertToInt(value):
    """convert to int
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- result
    """
    if value is None:
        return value
    try:
        return int(value)
    except ValueError:
        return None
        
def convertToFloat(value):
    """convert to float
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- result
    """
    if value is None:
        return value
    try:
        return float(value)
    except ValueError:
        return None

def processText(value):
    """process to get text, clean specifix character
    
    Arguments:
        value {string} -- input value
    
    Returns:
        string -- out put value
    """
    if value:
        value = replace_escape_chars(value)
        value = remove_tags(value)
        value = value.replace('#ft5_slash#', '/').replace('\\/', '/')
        return value
    else:
        return ''

def processHtml(value):
    """process to get text, clean specifix character
    
    Arguments:
        value {string} -- input value
    
    Returns:
        string -- out put value
    """
    if value:
        value = replace_escape_chars(value)
        value = value.replace('#ft5_slash#', '/')
        return value
    else:
        return ''

def processFloat(value):
    """process to get float value
    
    Arguments:
        value {string} -- input string
    
    Returns:
        float -- output value
    """
    if value:
        value = str(value)
        value = getMoney(value)
        return value
    else:
        return ''

def processInt(value):
    if value:
        value = getQuantity(value)
        return value
    else:
        return ''


def processMoney(value):
    """input_processor to extract money to float
    
    Arguments:
        value {string} -- input value
    
    Returns:
        float -- return money in float
    """
    if value:
        value = getMoney(value)
        return value
    else:
        return ''

def processQuantity(value):
    """input_processor to get quantity from a string
    
    Arguments:
        value {string} -- Input value
    
    Returns:
        int -- quantity
    """
    if value:
        value = getQuantity(value)
        return value
    else:
        return ''

def processEmail(value):
    emails = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', value)
    if emails:
        for email in emails:
            if email not in emails:
                emails.append(email)
    return emails


class JoinNotEmpty(object):
    def __init__(self, separator=u' '):
        self.separator = separator

    def __call__(self, values):
        result = list(filter(None, values)) 
        if len(result) > 0:
            return self.separator.join(result)
        else:
            return ''
        

class DataItem(scrapy.Item):
    
    url = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=TakeFirst()
    )

    cik = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=JoinNotEmpty('|')
    )
    accurate = scrapy.Field(
        input_processor=MapCompose(processText),
        output_processor=JoinNotEmpty('|')
    )
    