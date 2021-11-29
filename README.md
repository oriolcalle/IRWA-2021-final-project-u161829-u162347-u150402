# IRWA-2021-final-project-part-3


Introduction
Part 3 of the Search Engine project. Code designed to perform indexing, tf-idf weighting and tweet ranking (based on tf-idf score and our new custom score) for a given query on the tweet dataset that we processed in Part 1.
Part 2 and part 1 code is also provided.

Project Organization
├── README.md
├── data
│   └── dataset_tweets_WHO.txt
│
└── IRWA-2021-final-project-part-3.ipynb

Requirements:
Project developed in Python 3.7.12
These are the following packages needed to run this project:
	- collections
	- math
	- datetime
	- nltk (3.2.5)
	- json (2.0.9)
	- pycountry (20.7.3)
	- re (2.2.1)
	- numpy (1.19.5)
	- pandas (1.0.4)
	- sklearn (0.22.2.post1)
	- gensim (3.6.0)
	- matplotlib (3.2.2)



Usage:
The code should run perfectly if you start running cell by cell from the top, or do a run all.
This should be the order of execution:
	1. Deploy load_tweets()
	2. Deploy remove_stopwords(), stemming(), clean() (in this order)
	3. Run load_tweets() and store the output in the variable tweets
	4. For every tweet in tweets, perform the cleaning and store them in a variable filtered_tweets
	5. deploy create_index()
	6. Run create index for the filtered tweets.
	7. Deploy get_document_information()
	8. Run get_document_information() and store it in the variable doc_info, ans store the length of doc_info to num_documents
	9. Deploy create_index_tfidf()
	10. Run index,tf,df,idf = create_index_tfidf(filtered_tweets,num_documents)
	
Ranking Methods
	11. Deploy rank_tfidf()
	12. Deploy perform_date_substraction() and rank_custom()
	13. Deploy w2v_vector()
	14. Deploy rank_w2vec()

Evaluation
	15. Deploy search()
	16. Deploy perform_query()
	17. You can call perform_query() with a given query and method as parameters or just fill the input requests. Method 1 stands for tf-idf ranking, 2 stands for custom ranking and 3 for Word2Vec 

