import nltk
from datetime import datetime,date
from flask import Flask, render_template
from flask import request
import hashlib
from app.analytics.analytics_data import AnalyticsData, Click, Session, Query, User
from app.core import utils
from app.search_engine.search_engine import SearchEngine

import plotly
import plotly.express as px
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

app = Flask(__name__)

searchEngine = SearchEngine()
analytics_data = AnalyticsData()
corpus = searchEngine.tweets


@app.route('/')
def search_form():
    #create_fake_sessions() is used just to have some data in the dashboard, the data is dummy
    create_fake_sessions()

    IP = request.remote_addr
    browser = request.user_agent.browser
    platform = request.user_agent.platform
    
    if not user_exists(IP):
        time = get_current_datetime()
        analytics_data.fact_users.append(User(IP,time))
        print("New User with IP: {}, first time: {} ".format(IP,time))
        sessionID,time,ip_address = create_session()
        analytics_data.fact_sessions.append(Session(sessionID, time,IP,platform,browser,True))
        print("New Session for user with IP: {},sessionID {}, session start time: {},Platform/Browser: {}/{}  ".format(IP,sessionID,time,platform,browser))
    else:
        if is_last_session_30min(IP):
            new_sessionID,time,ip_address = create_session()
            print("New Session for user with IP: {},sessionID {}, session start time: {},Platform/Browser: {}/{}  ".format(IP,new_sessionID,time,platform,browser))
        

    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():

    search_query = request.form['search-query']
    query_length = len(search_query.split())
    datetime_ = get_current_datetime()
    
    # we should get current session value of user
    IP = request.remote_addr
    session = getLastSession(IP)

    analytics_data.fact_queries.append(Query(search_query, query_length ,datetime_,session.id))
    
    results = searchEngine.search(search_query)
    found_count = len(results)
    current_time = datetime.now().time().replace(microsecond=0)
    
    #change query spaces with + for link
    new_query = search_query.replace(" ", "+")
    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count,time=str(current_time),query = new_query)


@app.route('/doc_details', methods=['GET'])
def doc_details():

    args = request.args
    clicked_doc_id = int(request.args["id"])
    doc_rank = request.args["ranking"]
    previous = datetime.strptime(request.args["time"], '%H:%M:%S').time()
    now = datetime.now().time().replace(microsecond=0)

    elapsed_time = subtract_time(now,previous)
    IP = request.remote_addr
    session = getLastSession(IP)
    analytics_data.fact_clicks.append(Click(clicked_doc_id, "Click on result",elapsed_time.total_seconds(),session.id,doc_rank))

    print("User with session id= {} clicked in doc with id ={} - Time from result showed to click: {}".format(session.id,clicked_doc_id, elapsed_time.total_seconds()))
    
    #para el doc_clicked
    query = request.args["search_query"]
    doc_rank = request.args["ranking"]
    print(query) 
    print(doc_rank)
    return render_template('doc_details.html',doc=corpus[clicked_doc_id],query = query, rank = doc_rank,time = now)


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """
    ### Start replace with your code ###
    users = []
    session = []
    queries = []
    docs = []
    for u in analytics_data.fact_users:
        users.append("User IP: {}\nFirst time: {}".format(u.ip,u.first_time))

    for s in analytics_data.fact_sessions:
        session.append("User IP: {}\nSessionID {}\nSession start time: {}\nPlatform/Browser: {}/{}\nIs last session: {}  ".format(s.user_ip,s.id,s.session_start,s.platform,s.browser,s.is_last_Session))

    for q in analytics_data.fact_queries:
        queries.append("Query: {} \nSession ID: {}\nTime: {}".format(q.query_raw,q.session_id,str(q.query_datetime)))

    for clk in analytics_data.fact_clicks:
        docs.append((corpus[clk.doc_id]))

    return render_template('stats.html', clicks_data=docs,users_data = users,session_data = session,query_data = queries)
    ### End replace with your code ###

@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


@app.route('/dashboard')
def dashboard():
  
    #plot 1
    dictt = {}
    for clk in analytics_data.fact_clicks:
        if clk.doc_rank not in dictt.keys():
            dictt[clk.doc_rank] = [1,clk.dwell_time]
        else:
            dictt[clk.doc_rank] = [dictt[clk.doc_rank][0]+1,(dictt[clk.doc_rank][1]+clk.dwell_time)/2]
    
    plot_1x = []
    plot_1y1 = []
    plot_1y2 = []
    for key, value in dictt.items():
        plot_1x.append(key)
        plot_1y1.append(value[0])
        plot_1y2.append(value[1])

    #plot 2
    dictt = {}
    for ses in analytics_data.fact_sessions:
        if ses.platform not in dictt.keys():
            dictt[ses.platform] = 1
        else:
            dictt[ses.platform] = dictt[ses.platform]+1

    plot2x = list(dictt.keys())
    plot2y = list(dictt.values())
    
    #totals
    sessions_num = len(analytics_data.fact_sessions)
    queries_num = len(analytics_data.fact_queries)
    clicks_num = len(analytics_data.fact_clicks)
    users_num = len(analytics_data.fact_users)

    #plot 3
    dictt = {}
    for ses in analytics_data.fact_sessions:
        day = str(ses.session_start).split()[0]
        print(day)
        if day not in dictt.keys():
            dictt[day] = 1
        else:
            dictt[day] = dictt[day]+1

    plot3x = list(dictt.keys())
    plot3y = list(dictt.values())
    print(plot3x)
    print(plot3y)

    #plot 4
    dictt = {}
    for clk in analytics_data.fact_clicks:
        doc = clk.doc_id
        if doc not in dictt.keys():
            dictt[doc] = 1
        else:
            dictt[doc] = dictt[doc]+1

    plot4x = list(dictt.keys())
    plot4y = list(dictt.values())

    
    if plot4x != [] and plot4y !=[] :
        zipped_lists = zip(plot4y, plot4x)
        sorted_pairs = sorted(zipped_lists)
        tuples = zip(*sorted_pairs)
        plot4y, plot4x = [ list(tuple) for tuple in  tuples]

    print(plot4x)
    print(plot4y)



    return render_template('dashboard.html',plot1x = plot_1x,plot1y = plot_1y1
    ,plot2x = plot2x,plot2y = plot2y,total_sessions = sessions_num,total_queries = queries_num,
    total_users = users_num,total_clicks = clicks_num,plot3x = plot3x,plot3y = plot3y,
    plot4x = plot4x,plot4y = plot4y)

def create_session():
    time = get_current_datetime()
    ip_address = request.remote_addr
    lines = (str(time)+ip_address).encode('utf-8')
    sessionID = hashlib.md5(lines).hexdigest()
    return sessionID,time,ip_address


def subtract_time(now,previous):
    date_ = date(1, 1, 1)
    datetime1 = datetime.combine(date_, previous)
    datetime2 = datetime.combine(date_, now)
    return datetime2 - datetime1

def user_exists(ip):    
    return any( x.ip == ip for x in analytics_data.fact_users)

def getLastSession(ip):
    for i, e in reversed(list(enumerate(analytics_data.fact_sessions))):
        if (e.user_ip == ip) and (e.is_last_Session == True):
            return e

def is_last_session_30min(ip):
    last_session = getLastSession(ip)
    now = get_current_datetime()
    elapsed = now - last_session.session_start 
    if elapsed.total_seconds() > 1800: # 30*60
        last_session.is_last_Session = False
        return True
    else:
        return False

def get_current_datetime():
    return datetime.now().replace(microsecond=0)


def create_fake_sessions():
    x = datetime(2020, 12, 10)
    x2 = datetime(2020, 12, 11)
    x3 = datetime(2020, 12, 13)
    x4 = datetime(2020, 12, 14)
    x5 = datetime(2020, 12, 15)
    analytics_data.fact_sessions.append(Session(1, x,2,'windows','opera',False))
    analytics_data.fact_sessions.append(Session(1, x2,2,'android','chrome',False))
    analytics_data.fact_sessions.append(Session(1, x3,2,'macos','safari',False))
    analytics_data.fact_sessions.append(Session(1, x3,2,'windows','edge',False))
    analytics_data.fact_sessions.append(Session(1, x3,2,'windows','edge',False))
    analytics_data.fact_sessions.append(Session(1, x4,2,'iphone','safari',False))
    analytics_data.fact_sessions.append(Session(1, x5,2,'android','chrome',False))
    analytics_data.fact_sessions.append(Session(1, x5,2,'android','chrome',True))

if __name__ == "__main__":
    app.run(port="8088", host="0.0.0.0", threaded=False, debug=True)
