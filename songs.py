import pandas as pd
import matplotlib.pyplot as plt

songs=pd.read_csv(r"C:\Users\Malika Makker\Desktop\Bollywood-Data-master\wikipedia-data\songsDB.csv")

#print(songs)


year=songs["movieTitle_year"]

year=[x.split('_')[1] for x in year]

songs["movieTitle_year"]=year

#gender=songs["gender"]

#gender=[x for x in gender if (x=='MALE' or x=='FEMALE')] 


#songs["gender"]=gender

#print(gender)


#songs=songs.drop(songs[songs.gender!='MALE' and songs.gender!='FEMALE'].index)


print(songs.dtypes)

songs=songs[(songs.gender=='MALE') | (songs.gender=='FEMALE')]

print(songs)


songs=songs.drop(['singer_name'],axis=1)


#print(songs)

songs[['movieTitle_year']] = songs[['movieTitle_year']].astype(int)
songs[['song_count']] = songs[['song_count']].astype(int)

songs = songs.groupby(['movieTitle_year','gender'])['song_count'].sum()


print(songs)
#print(songs.dtypes)


final=songs.unstack()

print(final)

final.plot.bar()


plt.xlabel('Year')
plt.ylabel('Count')

plt.show()

'''
songs.plot.bar()

plt.show()


plt.figure()

ax=songs[['FEMALE','MALE']].plot.bar(x='movieTitle_year', y='song_count', rot=0,subplots=True)

plt.show()

'''



