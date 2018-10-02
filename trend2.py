import pandas as pd
import numpy as np
import scipy.interpolate as interpolate
import scipy.optimize as optimize
import pandas as pd
from sklearn.linear_model import LinearRegression

list_emo = ['angry', 'disgust', 'fear', 'sad', 'neutral', 'happy','surprise']
df= pd.read_csv("complete-data.csv", sep=',', encoding='utf-8')
df= df.sort_values(by='year')
df["emotion"] = df['emotion'].map(lambda emotion: list_emo.index(emotion))
man_df = df.loc[df['gender'] == 'man']
woman_df = df.loc[df['gender'] == 'woman']
print(woman_df)

man_df = man_df.groupby('year', as_index=False)['emotion'].mean()
woman_df = woman_df.groupby('year', as_index=False)['emotion'].mean()

X = man_df[['year']]
y = man_df['emotion']

model = LinearRegression(n_jobs=3)

model.fit(X, y)

print(model.predict([[2020]]))

X = woman_df[['year']]
y = woman_df['emotion']

model2 = LinearRegression(n_jobs=3)

model2.fit(X, y)

print(model2.predict([[2020]]))

import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
plt.plot(man_df["year"],man_df["emotion"],'g',label='Man', linewidth=5)
plt.plot(woman_df["year"],woman_df["emotion"],'c',label='Woman',linewidth=5)
plt.xlabel('Year')
plt.ylabel('Emotion')
plt.title('Emotion')
plt.plot(2020, model.predict([[2020]]), 'ro', label='Man Emotion Prediction')
plt.plot(2020, model2.predict([[2020]]), 'mo', label='Woman Emotion Prediction')
plt.legend()
plt.grid(True,color='k')
plt.show()
