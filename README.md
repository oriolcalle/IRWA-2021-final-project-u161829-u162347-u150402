# IRWA Final Project

## Description

Search engine web application for searching tweets in the dataset_tweets_WHO.txt file. 

## Project Organization 
 
├── README.md 
├── app 
│   ├── analytics 
│   │    └── analytics_data.py 
│   ├── core 
│   │    └── utils.py 
│   └── sear_engine 
│        ├── algorithms.py 
│        └── search_engine.py 
│ 
├── static 
│   ├── data 
│   │    └── dataset_tweets_WHO.txt 
│   ├── styles 
│   └── logo.png 
│ 
├── templates 
│   ├── base.html 
│   ├── dashboard.html 
│   ├── doc_details.html 
│   ├── index.html 
│   ├── results.html 
│   ├── sentiment.html 
│   └── stats.html 
│ 
├── README.md 
│ 
└── web_app.py 

### Dependencies 

Project developed in Python 3.10.0 
These are the following packages needed to run this project: 
Package         Version 
--------------- ---------- 
Faker           10.0.0 
Flask           2.0.2 
Jinja2          3.0.3 
nltk            3.6.5 
numpy           1.21.4 
pandas          1.3.4 
plotly          5.4.0 
pycountry       20.7.3 
python-dateutil 2.8.2 
scipy           1.7.3 


### Executing program

```
python .\web_app.py 
```



