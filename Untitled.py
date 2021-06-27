#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import configparser
import pandas as pd
import psycopg2



# In[2]:


config = configparser.ConfigParser()
config.read('cred.cfg')


# In[3]:


CLIENT_ID = config.items('AUTH')[0][1]
SECRET_KEY = config.items('AUTH')[1][1]


# In[4]:


auth = requests.auth.HTTPBasicAuth(CLIENT_ID,SECRET_KEY)


# In[5]:


pw = config.items('USER')[0][1]


# In[6]:


data = {
    'grant_type': 'password',
    'username' : 'saikirancvn',
    'password' : pw
}


# In[7]:


# Describe own headers, Any name and version
headers = {'User-Agent': 'crypto_trails/0.0.1'}


# In[8]:


res = requests.post('https://www.reddit.com/api/v1/access_token',
                   auth=auth,
                   data=data,
                   headers=headers)


# In[9]:


TOKEN = res.json()['access_token']


# In[10]:


headers['Authorization'] = f'bearer {TOKEN}'


# In[11]:


requests.get('https://oauth.reddit.com/api/v1/me',headers=headers) #200- Success


# In[22]:


df = pd.DataFrame()


# In[23]:


subreddit = 'bitcoin'
listing = 'hot' # Can be 'hot','new','best',etc


# In[24]:


res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{listing}',
                  headers=headers,
                  params={'limit':'100'
                          #,'before':'t3_o8bjr0'
                         })# Max is 100 posts, 'before' to get more posts 


# In[25]:


res.json()


# In[26]:


for post in res.json()['data']['children']:
    df = df.append({
        'user_id' : post['kind']+ '_' + post['data']['id'], #post['data']['author_fullname'],
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'text': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    },ignore_index=True)


# In[27]:


post['data'].keys()


# In[28]:


df


# In[29]:


df.iloc[4]['text']


# In[30]:


len(df['user_id'].unique())


# In[31]:


df[df.duplicated(subset='user_id', keep='first')].sort_values('user_id')


# In[33]:


df['downs'] = df['downs'].astype(float)
df['score'] = df['score'].astype(float)
df['ups'] = df['ups'].astype(float)
df['upvote_ratio'] = df['upvote_ratio'].astype(float)


# In[2]:

# connect to default database
conn = psycopg2.connect("host=127.0.0.1 dbname=saikirancvn user=postgres password=root")
conn.set_session(autocommit=True)
cur = conn.cursor()



# In[ ]:





# In[ ]:




