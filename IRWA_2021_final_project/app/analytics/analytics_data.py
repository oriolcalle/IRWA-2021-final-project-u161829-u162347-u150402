class AnalyticsData:
    fact_users = []
    fact_sessions = []
    fact_clicks = []
    fact_queries = []
    fact_documents = []

class User:
    def __init__(self, ip,time = None):
        self.ip = ip
        self.first_time = time

class Click:
    def __init__(self, doc_id, description,time ,session_id,rank):
        self.doc_id = doc_id
        self.description = description
        self.dwell_time = time
        self.doc_rank = rank
        self.session_id = session_id

class Session:
    def __init__(self, session_id, time,ip,platform,browser,is_last_Session):
        self.id = session_id
        self.session_start= time
        self.user_ip = ip
        self.platform = platform
        self.browser = browser
        self.is_last_Session = is_last_Session

class Query:
    def __init__(self, query_raw, num_terms,time,session_id):
        self.query_raw = query_raw
        self.num_terms = num_terms
        self.query_datetime = time
        self.session_id = session_id


