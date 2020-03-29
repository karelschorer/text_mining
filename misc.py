import os
import pandas as pd
import datetime
import helper_functions
from nltk.tokenize import sent_tokenize
os.chdir(r'C:\Users\Karel Schorer\PycharmProjects\textmining2')

def create_sentences(df, df_per_sentence):
    for index, row in df.iterrows():
        try:
            df.at[index, 'date'] = datetime.datetime.strptime(row['date'], '%m-%d-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

        for sentence in sent_tokenize(row['text']):
                df_per_sentence = df_per_sentence.append({'date':row['date'], 'text':sentence}, ignore_index=True)
    return df_per_sentence


def createGPEValidationSets():
    # Read files
    trump = pd.read_csv(r"Trump.csv", engine='python')
    obama = pd.read_csv(r"Obama.csv", engine='python')
    cities_countries = pd.read_json(r"cities_countries.json")

    ##### Clean Trump
    trump.drop(columns=['id_str', 'retweet_count', 'favorite_count'], inplace=True)
    trump.rename(columns={'created_at': 'date'}, inplace=True)

    ###### DELETE NAN'S IN TEXT ---> GAAT MIS BIJ PARSEN
    trump.dropna(subset=['text'], inplace=True)

    trump_per_sentence = pd.DataFrame(columns=['date', 'text'])
    trump_per_sentence = create_sentences(trump, trump_per_sentence)

    obama.drop(columns=['Username', 'Tweet Link', 'Retweets', 'Likes', 'TweetImageUrl', 'Image'], inplace=True)
    obama.rename(columns={'Date': 'date', 'Tweet-text': 'text'}, inplace=True)

    ###### DELETE NAN'S IN TEXT ---> GAAT MIS BIJ PARSEN
    obama.dropna(subset=['text'], inplace=True)

    obama_per_sentence = pd.DataFrame(columns=['date', 'text'])
    obama_per_sentence = create_sentences(obama, obama_per_sentence)

    trump_per_sentence['GPE'] = None
    obama_per_sentence['GPE'] = None

    trump_per_sentence['GPE'] = trump_per_sentence['text'].apply(lambda x: helper_functions.extract_GPEs(x))
    obama_per_sentence['GPE'] = obama_per_sentence['text'].apply(lambda x: helper_functions.extract_GPEs(x))

    trump_per_sentence.to_csv('TrumpGPEValidation.csv')
    obama_per_sentence.to_csv('ObamaGPEValidation.csv')

#createGPEValidationSets()

def finalGPEValidationSets():
    #import trump & obama validation + Scores. Vervolgens 150 lege GPE's pakken & 150 GPE's voor beide.
    obamaVader = pd.read_csv('ObamaScores.csv')
    trumpVader = pd.read_csv('TrumpScoresUpdated.csv')
    obamaGPE = pd.read_csv('ObamaGPEValidation.csv')
    trumpGPE = pd.read_csv('TrumpGPEValidation.csv')
    obamaGPE = obamaGPE[obamaGPE['GPE'].str.len() == 2]
    trumpGPE = trumpGPE[trumpGPE['GPE'].str.len() == 2]
    obamaGPESample = obamaGPE.sample(150)
    trumpGPESample = trumpGPE.sample(150)
    obamaVaderSample = obamaVader.sample(150)
    trumpVaderSample = trumpVader.sample(150)
    obamaGPEFinalSample = pd.concat([obamaGPESample, obamaVaderSample])
    trumpGPEFinalSample = pd.concat([trumpGPESample, trumpVaderSample])
    obamaGPEFinalSample.to_csv('obamaGPESample.csv')
    trumpGPEFinalSample.to_csv('trumpGPESample.csv')
    return 'done'

finalGPEValidationSets()

def sampleAndPresidentData():
    trump = pd.read_csv('TrumpScoresUpdated.csv')
    obama = pd.read_csv('ObamaScores.csv')
    trump.drop(72, inplace=True)
    trump.drop(129, inplace=True)
    obama_no_US = obama[obama['country'] != 'United States']
    trump_no_US = trump[trump['country'] != 'United States']
    obama = obama[(obama['country'] != 'Japan') & (obama['gpe'] != 'Obama')]
    # obama_no_US.to_csv('Obama_no_US.csv')
    return trump, obama, obama_no_US, trump_no_US


def createSamples(trump, obama):
    obama_positive = obama[obama['score'] > 0.33]
    obama_neutral = obama[obama['score'] < 0.33]
    obama_neutral = obama_neutral[obama_neutral['score'] > -0.33]
    obama_negative = obama[obama['score'] < -0.33]
    trump_positive = trump[trump['score'] > 0.33]
    trump_neutral = trump[trump['score'] < 0.33]
    trump_neutral = trump_neutral[trump_neutral['score'] > -0.33]
    trump_negative = trump[trump['score'] < -0.33]

    print(len(obama_negative))
    obama_sampled = pd.concat([obama_positive.sample(105), obama_neutral.sample(105), obama_negative])
    obama_sampled = obama_sampled[['text', 'gpe', 'country', 'score']]
    obama_sampled['classified'] = obama_sampled['score'].apply(lambda x: classify(x))
    trump_sampled = pd.concat([trump_positive.sample(100), trump_neutral.sample(100), trump_negative.sample(100)])
    trump_sampled = trump_sampled[['text', 'gpe', 'country', 'score']]
    trump_sampled['classified'] = trump_sampled['score'].apply(lambda x: classify(x))
    obama_sampled.to_csv('ObamaWithUs.csv')
    trump_sampled.to_csv('TrumpSample.csv')

def classify(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

#createSamples(sampleAndPresidentData()[3],  sampleAndPresidentData()[1])

#print(trump_sampled)
'''
trump['date'] = trump['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
trump_no_president = trump[trump['date'] < datetime.datetime(year=2017, month=1, day=1)]
trump_president = trump[trump['date'] >= datetime.datetime(year=2017, month=1, day=1)]
trump_no_president.to_csv('trump_no_president.csv')
trump_president.to_csv('trump_president.csv')

print(obama['date'])
obama['date'] = obama['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d_%H:%M'))
obama_no_president = obama[obama['date'] >= datetime.datetime(year=2017, month=1, day=1)]
obama_president = obama[obama['date'] < datetime.datetime(year=2017, month=1, day=1)]
obama_no_president.to_csv('obama_no_president.csv')
obama_president.to_csv('obama_president.csv')
'''