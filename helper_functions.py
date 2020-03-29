# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 16:02:00 2020

@author: maxni
"""
import urllib
import urllib.parse
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import xml.etree.cElementTree as ET
from lxml import etree
import time
import json
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm') #en
import nltk
from nltk.sentiment import vader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader_model = SentimentIntensityAnalyzer()
from geopy.exc import GeocoderTimedOut
import geopy.geocoders
from geopy.extra.rate_limiter import RateLimiter



#NER with spacy

def extract_GPEs(sentence):
    
    list_of_gpes = []
    doc = nlp(sentence)
    displacy.render(doc, jupyter=False, style='ent')
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            list_of_gpes.append(ent.text)
    return list_of_gpes

#entities must be between [[]]
def locationLinking(new_content):
    import ssl
    try:
        #for initial implementation: Remove when using in final pipeline
        new_content = '[[' + new_content + ']]'
        context = ssl._create_unverified_context()
        #new_content = '[[Netherlands]]'
        aida_url = "https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate"
        params={"text": new_content, "tag_mode": 'manual'}
        request = Request(aida_url, urlencode(params).encode())
        # AIDA returns a json structure
        this_json = urlopen(request, context=context).read().decode('unicode-escape')
        results=json.loads(this_json)
        print(results)

        dis_entities={}
                # We iterate over the data elements "mentions" in the json results
        for dis_entity in results['mentions']:
           # print(dis_entity)
            ## AIDI labels the bestEntity in the json
            if 'bestEntity' in dis_entity.keys():
                best_entity=dis_entity['bestEntity']['kbIdentifier']
                clean_url=best_entity[5:] #SKIP YAGO:
            else:
                clean_url='NIL'
            dis_entities[str(dis_entity['offset'])] = clean_url # BECOMES THE VALUE IN THE DICTIONARY FOR THE OFFSET(REPRESENTING THE START OF THE MENTION) IN THE TEXT
        return (dis_entities[str(results['mentions'][0]['offset'])], new_content)
    except:
        return new_content


#import geopy
def getCountry(text):
    #geo_keys = 'name1', 'name2', 'name3', 'name4', 'name5', n
   # ]  # Put in your API keys as strings
    key = 'AkuTMRwxGjK2-wtHvgeCMcAoYBVvEB0XF0CaW-q_7u2EHSIfVhKHCwlD5FtF63FR'
    if text[0] == 'NIL':
        value = text[1]
    else:
        value = text[0]
    from geopy.geocoders import Bing
    #geopy.geocoders.options.default_proxies = {"http": "http://37.48.118.4:13010"}
    geolocator = Bing(api_key=key)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geocode(value)
    if location is not None:
        location = location.raw
    else:
        return 'None'
    #geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)
    #lat = location['lat']
    #lon = location['lon']
    #location = geocode((lat, lon), language='en', exactly_one=True)
    #location = location.raw
    #country = location['address']['country']
    try:
        country = location['address']['countryRegion']
        return country
    except KeyError:
        return text

def get_vader(sentence): #calculates vader score, returns positive or compound?
    vader_output=vader_model.polarity_scores(sentence)
    #vader_label = vader_output_to_label(vader_output)
    compound = vader_output['compound']
    return compound
