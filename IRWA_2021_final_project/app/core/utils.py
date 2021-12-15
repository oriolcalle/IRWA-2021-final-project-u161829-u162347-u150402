import nltk
from datetime import datetime,date
from flask import Flask, render_template
from flask import request
import hashlib

import plotly
import plotly.express as px
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json
from random import random

from faker import Faker

fake = Faker()


# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


class Document:
    def __init__(self, id, title, description, doc_date, email, ip):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.email = email
        self.ip = ip


def load_documents_corpus():
    """
    Load documents corpus from dataset_tweets_WHO.txt file
    :return:
    """

    ##### demo replace ith your code here #####
    docs = []
    for i in range(200):
        docs.append(Document(fake.uuid4(), fake.text(), fake.text(), fake.date_this_year(), fake.email(), fake.ipv4()))
    return docs


def getSession():
    time = datetime.now().replace(microsecond=0)
    ip_address = request.remote_addr
    lines = (str(time)+ip_address).encode('utf-8')
    sessionID = hashlib.md5(lines).hexdigest()
    return sessionID,time,ip_address

def create_plot():
    df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']})
    fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def subtract_time(now,previous):
    date_ = date(1, 1, 1)
    datetime1 = datetime.combine(date_, previous)
    datetime2 = datetime.combine(date_, now)
    return datetime2 - datetime1

