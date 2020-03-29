# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 10:19:37 2020

@author: maxni
"""

import pandas as pd
import os
import datetime
from nltk.tokenize import sent_tokenize
import helper_functions

os.chdir(r'C:\Users\Karel Schorer\PycharmProjects\textmining2')

# Read files
trump = pd.read_csv(r"Trump.csv", engine='python')
#obama = pd.read_csv(r"Obama.csv", engine='python')
cities_countries = pd.read_json(r"cities_countries.json") 

##### Clean Trump
trump.drop(columns=['id_str', 'retweet_count', 'favorite_count'], inplace=True)
trump.rename(columns={'created_at': 'date'}, inplace=True)

###### DELETE NAN'S IN TEXT ---> GAAT MIS BIJ PARSEN
trump.dropna(subset=['text'], inplace=True)

trump_per_sentence = pd.DataFrame(columns=['date', 'text'])

def create_sentences(df, df_per_sentence):
    for index, row in df.iterrows():
        try:
            df.at[index, 'date'] = datetime.datetime.strptime(row['date'], '%m-%d-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

        for sentence in sent_tokenize(row['text']):
                df_per_sentence = df_per_sentence.append({'date':row['date'], 'text':sentence}, ignore_index=True)
    return df_per_sentence

trump_per_sentence = create_sentences(trump, trump_per_sentence)
    
##### Clean Obama      
#obama.drop(columns=['Username', 'Tweet Link', 'Retweets', 'Likes', 'TweetImageUrl', 'Image'], inplace=True)
#obama.rename(columns={'Date': 'date', 'Tweet-text': 'text'}, inplace=True)

###### DELETE NAN'S IN TEXT ---> GAAT MIS BIJ PARSEN
#obama.dropna(subset=['text'], inplace=True)

#obama_per_sentence = pd.DataFrame(columns=['date', 'text'])
#obama_per_sentence = create_sentences(obama, obama_per_sentence)
# Trump words frequencies
        
trump_per_sentence['GPE'] = None
#obama_per_sentence['GPE'] = None

trump_per_sentence['GPE'] = trump_per_sentence['text'].apply(lambda x: helper_functions.extract_GPEs(x))
#obama_per_sentence['GPE'] = obama_per_sentence['text'].apply(lambda x: helper_functions.extract_GPEs(x))

#alternatief: hele tweet overnemen met [[]] om GPE's en dan in getCountry(locationLinking()) 
#stoppen, voor bijvoorbeeld San Juan in Argentinië

#trump.to_hdf('trump.h5')
#obama.to_hdf('obama.h5')
##Obama 
#obama_tweets_per_country = pd.DataFrame(columns=['date', 'text', 'gpe'])

def obama(obama_per_sentence, obama_tweets_per_country, startIndex= 0):
    for index, row in obama_per_sentence.iterrows():
        #obama_per_sentence.loc[index, 'GPE'] = (row['GPE'].strip('][').split(', '))
        for gpe in row['GPE']:
            obama_tweets_per_country = obama_tweets_per_country.append({'date': row['date'], 'text': row['text'],
                                                                        'gpe':gpe}, ignore_index=True)
    for index, country in obama_tweets_per_country['gpe'].iteritems():
        try:
            if startIndex <= index:
                obama_tweets_per_country.loc[index, 'country'] = \
                    helper_functions.getCountry(helper_functions.locationLinking(country))
                print('done', index)
        except:
            obama_tweets_per_country.to_csv(r"C:\Users\Karel Schorer\PycharmProjects\textmining2\ObamaScores.csv")
            print(index)
    return obama_tweets_per_country

#obama_tweets_per_country = obama(obama_per_sentence, obama_tweets_per_country)
#obama_tweets_per_country['score'] = obama_tweets_per_country['text'].apply(lambda x: helper_functions.get_vader(x))

trump_tweets_per_country = pd.DataFrame(columns=['date', 'text', 'gpe'])
##Obama 
def trump(trump_per_sentence, trump_tweets_per_country, startIndex = 0):
    for index, row in trump_per_sentence.iterrows():
        # obama_per_sentence.loc[index, 'GPE'] = (row['GPE'].strip('][').split(', '))
        for gpe in row['GPE']:
            trump_tweets_per_country = trump_tweets_per_country.append({'date': row['date'], 'text': row['text'],
                                                                        'gpe': gpe}, ignore_index=True)
    for index, country in trump_tweets_per_country['gpe'].iteritems():
        try:
            if startIndex <= index:
                trump_tweets_per_country.loc[index, 'country'] = \
                    helper_functions.getCountry(helper_functions.locationLinking(country))
                print('done', index)
            if index in {1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000}:
                trump_tweets_per_country.to_csv(r"C:\Users\Karel Schorer\PycharmProjects\textmining2\TrumpScoresUpdated.csv")
        except:
            trump_tweets_per_country.to_csv(r"C:\Users\Karel Schorer\PycharmProjects\textmining2\TrumpScoresUpdated.csv")
            print(index)
    return trump_tweets_per_country



trump_tweets_per_country = trump(trump_per_sentence, trump_tweets_per_country)
trump_tweets_per_country['score'] = trump_tweets_per_country['text'].apply(lambda x: helper_functions.get_vader(x))


#Export to csv

#obama_tweets_per_country.to_csv(r"C:\Users\Karel Schorer\PycharmProjects\textmining2\ObamaScores.csv")
trump_tweets_per_country.to_csv(r"C:\Users\Karel Schorer\PycharmProjects\textmining2\TrumpScoresUpdated.csv")