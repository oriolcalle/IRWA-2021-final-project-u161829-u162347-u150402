import json
import re
import pycountry
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

from collections import defaultdict
from array import array
import numpy as np

nltk.download('stopwords')


#####################################################################################################################################

def own_remove_stopwords(string,language):
    stop_words = set(stopwords.words(language))
    return [word for word in string if not word.lower() in stop_words]

def stemming(string,language):
    porter_stemmer = PorterStemmer()
    if language in SnowballStemmer.languages:
        snowball_stemmer = SnowballStemmer(language)
        return [snowball_stemmer.stem(word) for word in string]
    else:
        return [porter_stemmer.stem(word) for word in string]

def clean(string,language='en'):

    string = string.lower()
    string = string.split() #tokenize
    string = [re.sub("[^a-z0-9#@]","",word) for word in string] #we remove everything except words, numbers # and @.
    string = [word for word in string if word != ''] # we delete the token that are empty.
    try:
      if len(language) == 2:
              language = pycountry.languages.get(alpha_2=language).name.lower()
      elif len(language) == 3:
              language = pycountry.languages.get(alpha_3=language).name.lower()  
      string = own_remove_stopwords(string,language)
    except:
      string = own_remove_stopwords(string,'english')

    string = stemming(string,language)   #stemming
    
    return string


#####################################################################################################################################



class Tweet:
    def __init__(self, id, jsonTweet):
        self.id = id
        self.title = jsonTweet['full_text'][:20]
        self.screen_name = jsonTweet['user']['screen_name']
        self.username = jsonTweet['user']['name']
        self.description = jsonTweet['full_text']
        self.tweet_date = jsonTweet['created_at']
        self.lang = jsonTweet['lang']
        self.source = jsonTweet['source']
        self.favorite_count = jsonTweet['favorite_count']
        self.retweet_count = jsonTweet['retweet_count']
        self.url = "https://twitter.com/%s/status/%s" % (jsonTweet['user']['screen_name'], jsonTweet['id_str'])
        self.rawjson = jsonTweet
        hashtags = []
        for x in jsonTweet['entities']['hashtags']:
            hashtags.append(x['text'])
        self.hashtags = hashtags
        self.rank = 0

def load_tweets_corpus():
  path = 'static/data/dataset_tweets_WHO.txt'
  with open(path,"r",encoding='utf-8') as file:
        data = json.load(file)
  
  return [Tweet(tweet[0],tweet[1]) for tweet in data.items()]


#####################################################################################################################################

def create_index(tweets):
    index = defaultdict(list)
    for tweet in tweets:  
        tweet_id = int(tweet.id)

        current_page_index = {}
        for position, term in enumerate(tweet.description): # terms contains page_title + page_text. Loop over all terms
            try:
                current_page_index[term][1].append(position)  
            except:
                current_page_index[term]=[tweet_id, array('I',[position])] #'I' indicates unsigned int (int in Python)
        for term_page, posting_page in current_page_index.items():
            index[term_page].append(posting_page)
    return index


#####################################################################################################################################

def rank_custom(docs,doc_info):
    query_vector = [0.5, 0.5]
    custom_scores = [[np.dot(query_vector, [doc_info[int(doc)].favorite_count,doc_info[int(doc)].retweet_count]), doc] for doc in docs]
    return custom_scores

def searchTweets(tweets, index, query='vaccine',language='en'):

    query = clean(query,language)
    docs = [set()] * len(query)
    for i, term in enumerate(query):
        try:
            termDocs=[posting[0] for posting in index[term]]
            docs[i] = set(termDocs)
        except:
            pass
    
    try:
        docs = list(set.intersection(*docs))
    except:
        pass
    
    doc_scores = rank_custom(docs, tweets)
  
    doc_scores.sort(reverse=True)
    
    ranked_docs = [x[1] for x in doc_scores]
        
    out = []
    for index in range(len(ranked_docs[:20])):
        tweets[ranked_docs[index]].rank = index+1
        out.append(tweets[ranked_docs[index]])
    return out

#####################################################################################################################################

