#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 17:01:44 2020

@author: rosalievanderwoude
"""

import pandas as pd

trump = pd.read_csv('Trump.csv')
obama = pd.read_csv('Obama.csv')

#NER with spacy
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

doc = nlp('Throwback is a beautiful city')
displacy.render(doc, jupyter=False, style='ent')
print(ent.text, ent.label_)

print(doc.ents)

for ent in doc.ents:
    if ent.label_ == 'GPE':
        print(ent.text, ent.label_)

for token in doc:
    print(token.text, token.tag_)

import nltk
from nltk.chunk import ne_chunk
nltk.download() 

sentences = nltk.sent_tokenize('mexico is a beautiful city')
for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    tokens_pos_tagged = nltk.pos_tag(tokens)
    tokens_pos_tagged_and_named_entities = ne_chunk(tokens_pos_tagged)
    print()
    print('ORIGINAL SENTENCE', sentence)
    print('NAMED ENTITY RECOGNITION OUTPUT', tokens_pos_tagged_and_named_entities)







# worldmap

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import helpers
import slug

from geonamescache import GeonamesCache  #pip install geonamescache
from helpers import slug 
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap

filename = 'csv/ag.lnd.frst.zs_Indicator_en_csv_v2/ag.lnd.frst.zs_Indicator_en_csv_v2.csv'
shapefile = 'shp/countries/ne_10m_admin_0_countries_lakes'
num_colors = 9
year = '2012'
cols = ['Country Name', 'Country Code', year]
title = 'Forest area as percentage of land area in {}'.format(year)
imgfile = 'img/{}.png'.format(slug(title))

description = ''.strip()     

test = pd.DataFrame(['Holland', 'Denmark', 'Italy', 'Throwback', 'Australia'])
import geonamescache

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
# print countries dictionary
print(countries)

   
from geonamescache.mappers import country
mapper = country(from_key='name', to_key='iso3')

iso3 = mapper('Amsterdam') # iso3 is assigned ESP




import cartopy.crs as ccrs

import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
import itertools
import numpy as np

shapename = 'admin_0_countries'
countries_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)

# some nice "earthy" colors
earth_colors = np.array([(199, 233, 192),
                                 (161, 217, 155),
                                (116, 196, 118),
                                (65, 171, 93),
                                (35, 139, 69),
                                ]) / 255.
earth_colors = itertools.cycle(earth_colors)

ax = plt.axes(projection=ccrs.PlateCarree())

for country in shpreader.Reader(countries_shp).records():
    print(country.attributes['NAME_LONG'], earth_colors.next())
    ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                      facecolor=earth_colors.next(),
                      label=country.attributes['NAME_LONG'])

plt.show()



import geopandas as pd






