from app.search_engine.algorithms import *


class SearchEngine:

    def __init__(self) -> None:
        self.tweets = load_tweets_corpus()
        filtered_tweets = []
        for tweet in self.tweets:
            tw = Tweet(tweet.id,tweet.rawjson)
            tw.description = clean(tweet.description,tweet.lang)
            filtered_tweets.append(tw)

        self.index = create_index(filtered_tweets)


    def search(self, search_query):
        print("Search query:", search_query)
        return searchTweets(self.tweets,self.index,search_query)

