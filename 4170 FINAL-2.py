#!/usr/bin/env python
# coding: utf-8

# # SPOTIFY WRAP 
# by ABHISHEK SHRESTHA

#                                                                              DATA VISUALIZATION CIS 4170

# In[2]:


pip install spotipy --upgrade #install spotipy packages 


# In[3]:


pip install -U spotify #install spotify packages 


# In[4]:


pip install -U git+https://github.com/mental32/spotify.py #egg=spotify


# In[5]:


import pandas as pd 
import numpy as np 
import json
import datetime
from datetime import timedelta 


# In[6]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[7]:


import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import plotly.graph_objects as go


# In[8]:


#import webbrowswer

import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotify.sync as spotify 


# Importing JSON file to a DataFrame 

# In[9]:


#Import the data from a json file 

with open('StreamingHistory0.json', encoding='utf8') as f: data = json.load(f)
print(data[:1])


# In[10]:


#Convert from json to a dataframe 

streamingHistory0 = pd.DataFrame()
def extract_json_value(column_name):
    return [i[column_name] for i in data]

streamingHistory0['artist_name'] = extract_json_value('artistName')
streamingHistory0['track_name'] = extract_json_value('trackName')
streamingHistory0['ms_played'] = extract_json_value('msPlayed')
streamingHistory0['end_time'] = extract_json_value('endTime')


# In[11]:


streamingHistory0.info()


# In[12]:


#Import the data from a json file 

with open('StreamingHistory1.json', encoding='utf8') as f: data = json.load(f)
print(data[:1])


# In[13]:


#Convert from json to a dataframe 

streamingHistory1 = pd.DataFrame()
def extract_json_value(column_name):
    return [i[column_name] for i in data]

streamingHistory1['artist_name'] = extract_json_value('artistName')
streamingHistory1['track_name'] = extract_json_value('trackName')
streamingHistory1['ms_played'] = extract_json_value('msPlayed')
streamingHistory1['end_time'] = extract_json_value('endTime')


# In[14]:


streamingHistory1.info()


# In[15]:


#Import the data from a json file 

with open('StreamingHistory2.json', encoding='utf8') as f: data = json.load(f)
print(data[:1])


# In[16]:


#Convert from json to a dataframe 

streamingHistory2 = pd.DataFrame()
def extract_json_value(column_name):
    return [i[column_name] for i in data]

streamingHistory2['artist_name'] = extract_json_value('artistName')
streamingHistory2['track_name'] = extract_json_value('trackName')
streamingHistory2['ms_played'] = extract_json_value('msPlayed')
streamingHistory2['end_time'] = extract_json_value('endTime')


# In[17]:


streamingHistory2.info()


# Merging Three Data Sets

# In[18]:


streamingHistory = streamingHistory0.append(streamingHistory1).append(streamingHistory2)


# In[19]:


streamingHistory


# To Time Stamp format 

# In[20]:


#Converting end_time to timestamp format

streamingHistory['end_time'] = pd.to_datetime(streamingHistory['end_time'])
streamingHistory.head(6)


# In[21]:


streamingHistory.dtypes


# In[22]:


streamingHistory = streamingHistory.sort_values(by=['end_time'], ascending = True)
streamingHistory.head()


# Converting end_time to Week Days

# In[26]:


def get_week_endpoints(df):
    days = df['end_time'].weekday()
    week_start = df['end_time'] - timedelta(days)
    week_end = week_start + timedelta(days=6)
    df['Week'] = str(week_start.strftime('%Y/%m/%d')) + ' - ' + str(week_end.strftime('%Y/%m/%d'))
    return df


# In[27]:


#streamingHistory['week'] = streaming_hist['endTime'].dt.week
streamingHistory = streamingHistory.apply(lambda x: get_week_endpoints(x), axis =1)


# In[28]:


streamingPlot = streamingHistory.groupby(by=['Week'], as_index=False)['ms_played'].agg(sum)
streamingPlot['mean'] = np.mean(streamingPlot.ms_played)                                                                                   


# In[29]:


import matplotlib.pyplot as plt


# In[32]:


def count_avg_plot(df, X, Y, title,  Z=None):
    ax = df.plot(x=X, y=Y, legend=False, figsize=(15,10), fontsize = 12, title=title, rot = 45, marker = 'o')
    ax.grid(True)
    ax.set_ylabel(Y)
    #ax.annotate("Point 1", (43, 91249856))
    ax.text(43, 91249856,'Average Minutes Played',horizontalalignment='right', fontsize = 'small')
    ax.title.set_size(20)
    if Z:
        ax2 = ax.twinx()
        ax2.set_ylabel(Z)
        df.plot(x=X, y=Z, ax=ax2, legend=False, color="r", linestyle='--', fontsize=15).grid(False)
        ax2.get_yaxis().set_visible(False)
        ax.figure.legend(loc=4)
        #ax.xticks(fontsize=14)
    plt.show()


# In[33]:


count_avg_plot(streamingPlot, 'Week', 'ms_played', 'Streaming History 2020-2021', 'mean')


# Seperating types into Music or Podcast

# In[34]:


streamingHistory = streamingHistory[streamingHistory.ms_played > 10000]


# In[35]:


streamingHistory.sort_values(by=['end_time'], ascending=True).head()
quarantine = streamingHistory.loc[streamingHistory.end_time > '2020-03-11']
regular = streamingHistory.loc[streamingHistory.end_time < '2020-03-11']


# In[36]:


pods = np.unique(quarantine[quarantine.ms_played > 720000]['artist_name'])
quarantine['Type'] = np.where(quarantine.artist_name.isin(pods), 'Podcast', 'Music')


# In[37]:


for val in pods:
    print(val)


# In[38]:


regular['Type'] = np.where(regular.artist_name.isin(pods), 'Podcast', 'Music')
quarantine['Type'] = np.where(quarantine.artist_name.isin(pods), 'Podcast', 'Music')
regular.head()


# In[39]:


regular_artists_music = np.unique(regular[regular.Type.isin(['Music'])]['artist_name'].values)
regular_pods = np.unique(regular[regular.Type.isin(['Podcast'])]['artist_name'].values)

qtine_artists_music  = np.unique(quarantine[quarantine.Type.isin(['Music'])]['artist_name'].values)

qtine_pods  = np.unique(quarantine[quarantine.Type.isin(['Podcast'])]['artist_name'].values)

new_discoveries_music = [artist for artist in qtine_artists_music if artist not in regular_artists_music]
len(np.unique(new_discoveries_music))


# In[40]:


len(qtine_artists_music)


# In[41]:


new_discoveries_music


# In[42]:


quarantine[quarantine.artist_name.isin(new_discoveries_music)].groupby(by='artist_name', as_index=False)['ms_played'].agg(sum).sort_values(by='ms_played', ascending = False).head(10)


# In[43]:


new_pods = [artist for artist in qtine_pods if artist not in regular_pods]
len(new_pods)


# In[44]:


quarantine


# In[45]:


quarantine.head()


# In[46]:


group_type = quarantine.groupby(by='Type', as_index=False)['ms_played'].agg(sum)

group_type


# Music v. Podcast 

# In[47]:


labels = 'Music', 'Podcast'
sizes = [2349789563, 663977974]
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Podcast')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# Popularity of artist based on the number of times their songs were clicked and played

# In[74]:


most_played_artists_by_count = streamingHistory.groupby(by='artist_name')['track_name'].count().sort_values(ascending=False)[:10]

print('The most popular artists by number of times their songs were played were: \n\n{}'.format(most_played_artists_by_count))


# In[49]:


colors = ['RGB(103, 0, 31)','RGB(178, 24, 43)','RGB(214, 96, 77)','RGB(244, 165, 130)','RGB(253, 219, 199)',
          'RGB(247, 247, 247)','RGB(209, 229, 240)','RGB(146, 197, 222)','RGB(67, 147, 195)','RGB(33, 102, 172)',
          'RGB(5, 48, 97)']


layout = go.Layout(
    title='Popularity Of Artists By Number Of Times Their Song Was Played',
    yaxis= dict(
        title="Number of Times Played",
        gridcolor='rgb(255, 255, 255)',
        zerolinewidth=1,
        ticklen=5,
        gridwidth=2,
        titlefont=dict(size=15)),
    xaxis=dict(title="Artist Name"))


fig = go.Figure(data=[go.Bar(x=most_played_artists_by_count.index,
                             y=most_played_artists_by_count,
                             textposition='auto',
                             opacity=1,
                             marker_color=colors)])
fig.show()


# Top Streamed Artists

# In[50]:


sum(quarantine['ms_played'])/60000


# In[51]:


quarantine_music = quarantine[quarantine.Type.isin(['Music'])]


# In[52]:


artists = quarantine_music.groupby(['artist_name'], as_index=False)['ms_played'].agg(sum).sort_values(by=['ms_played'], ascending=False).head(10)


# In[53]:


import seaborn as sns 
sns.set(rc={'figure.figsize':(16,10)})
sns.set(style="whitegrid")
sns.set(font_scale=1.5) 
g = sns.barplot(x="artist_name", y="ms_played", data=artists)
g.set_title('Top Streamed Artists')
g.set_xticklabels(g.get_xticklabels(),rotation=30)


# Top Artist 

# In[54]:


artist = streamingHistory0.append(streamingHistory1).append(streamingHistory2)
artist['minutes_played'] = artist.ms_played.divide(60000)
artist.drop('ms_played', axis=1, inplace=True)
artist.drop('end_time', axis=1, inplace=True)

artist.head()


# In[55]:


artist_1 = artist.drop_duplicates(subset = ["track_name"])
artist_1.drop('minutes_played', axis=1, inplace=True)
artist_1


# In[56]:


artist_1 = artist_1.groupby(['artist_name'], as_index = False).count()

artist_1


# In[57]:


artist_1 = artist_1.rename(columns={"track_name": "unique_songs"})
artist_1.head()


# In[58]:


time = artist.groupby(['artist_name'], as_index=False).sum()

time.head()


# Top 10 Artist based on Unique Songs 

# In[59]:




top_artist = pd.merge(artist_1, time, on='artist_name')
top_artist = top_artist.sort_values(by='unique_songs', ascending=False).head(10)
top_artist


# In[60]:


fig = px.scatter(top_artist, x="artist_name", y="minutes_played", title='Top 10 of Most Played Artists by Songs', size="unique_songs", color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()


# Most listened to Song 

# In[75]:



song = streamingHistory0.append(streamingHistory1).append(streamingHistory2)
song['minutes_played'] = song.ms_played.divide(60000)
song.drop('ms_played', axis=1, inplace=True)
song


# In[62]:


song = song.groupby(['track_name'], as_index=False).sum()
song = song.sort_values(by='minutes_played', ascending=False)
song


# In[63]:


song_artist = streamingHistory0.append(streamingHistory1).append(streamingHistory2)
song_artist = song_artist.sort_values(by='track_name', ascending=False)
song_artist.drop('end_time', axis=1, inplace=True)
song_artist.drop('ms_played', axis=1, inplace=True)
song_artist.head(10)


# In[64]:


song_artist = song_artist.drop_duplicates(subset = ["track_name"])
song_artist


# In[65]:


song = pd.merge(song_artist, song, on='track_name')
song = song.sort_values(by='minutes_played', ascending=False)
song


# In[66]:


song = song.sort_values(by='minutes_played', ascending=False).head(16)
song.reset_index(inplace = True, drop = True) 
song


# Top 15 Songs listened to

# In[67]:


fig = px.bar(song, x="track_name", y="minutes_played", title = 'Song Listened to the Most', color = "artist_name", color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()


# In[68]:


#Top 50 Songs

top_50 = streamingHistory0.append(streamingHistory1).append(streamingHistory2)
top_50['minutes_played'] = top_50.ms_played.divide(60000)
top_50.drop('ms_played', axis=1, inplace=True)
top_50


# In[69]:


top_50 = top_50.groupby(['track_name'], as_index=False).sum()
top_50 = top_50.sort_values(by='minutes_played', ascending=False).head(51)
top_50.reset_index(inplace = True, drop = True) 
top_50


# In[70]:


fig = px.scatter(top_50, x="track_name", y="minutes_played", title="Top 50 Songs")
fig.show()


# In[ ]:




