import pandas as pd
import numpy as np
import sys

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def getTextSentiment(message_text):
    sid = SentimentIntensityAnalyzer()
    print(message_text)
    scores = sid.polarity_scores(message_text)
    print(scores["compound"])
    return scores["compound"]

colnames=['year','adjective']
woman_df= pd.read_csv("female_adjectives.csv", names=colnames, header=None , sep=',', encoding='utf-8')
man_df= pd.read_csv("male_adjectives.csv", names=colnames, header=None , sep=',', encoding='utf-8')
sys.__stdout__ = sys.stdout

man_df = man_df.groupby('year').apply(lambda x: pd.Series({'adjective': "%s" % ', '.join(x['adjective'])}))
#print(man_df2)

list_man_sent = []
for value in man_df['adjective']:
    list_man_sent.append(getTextSentiment(value))
man_df["Sentiment"]=list_man_sent
print(man_df)



woman_df = woman_df.groupby('year').apply(lambda x: pd.Series({'adjective': "%s" % ', '.join(x['adjective'])}))
list_woman_sent = []
for value in woman_df['adjective']:
    list_woman_sent.append(getTextSentiment(value))
woman_df["Sentiment"]=list_woman_sent

import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
plt.plot(man_df.index.values,man_df["Sentiment"],'g',label='Man', linewidth=2)
plt.plot(woman_df.index.values,woman_df["Sentiment"],'c',label='Woman',linewidth=2)
plt.xlabel('Year')
plt.ylabel('Sentiment')
plt.title('Sentiment')
#plt.plot(2020, model.predict([[2020]]), 'ro', label='Man Emotion Prediction')
#plt.plot(2020, model2.predict([[2020]]), 'mo', label='Woman Emotion Prediction')
plt.legend()
plt.grid(True,color='k')
plt.show()
