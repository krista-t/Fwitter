from bottle import response
import sqlite3



TRENDS = [
  {"category": "Music", "title": "We Won", "tweets_counter": "135K"},
  {"category": "Pop", "title": "Blue Ivy", "tweets_counter": "40k"},
  {"category": "Trending in US", "title": "Denim Day", "tweets_counter": "40k"},
  {"category": "Ukraine", "title": "Ukraine", "tweets_counter": "20k"},
  {"category": "Russia", "title": "Russia", "tweets_counter": "10k"},
]

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

COOKIE_SECRET = "SA6a$mLMH76%"
##############################


##############################
# create json in sqliteDB
def create_json_from_sqlite_result(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

##############################
# connect database
def _db_connect(db_name):
    db = sqlite3.connect(db_name)
    db.row_factory = create_json_from_sqlite_result
    return db

##############################
# error messages
ERROR = {
    "error_name_min": "name at least 2 characters",
    "error_name_max": "name less than 20 characters",
    "error_email": "error, enter email",
    "error_email_re": "error, enter correct email form",
    "error_email_exists": "email already exists",
    "error_password_min": "password must be at least 6 characters",
    "error_password": "enter password",
    "error_img": "wrong image format, only png, jpg, jpeg allowed",
}

##############################
##DB QUERIES##
#singup queries
USER_NAME_QUERY = """
SELECT user_name FROM users where user_name=?
"""
USER_EMAIL_QUERY = """
SELECT user_email FROM users where user_email= ?
"""
#login query
USER_NAME_PASS_QUERY = """
SELECT user_name, user_password FROM users where user_name= ?
"""
#delete session query
DELETE_SESS_ROW_QUERY = """
DELETE FROM sessions WHERE session_id= ?"""

#delete tweet query
DELETE_TWEET_QUERY = """
DELETE FROM tweets WHERE tweet_id= ?"""

#show tweet with specific id query
GET_TWEET_WITH_ID_QUERY = """
SELECT * FROM tweets WHERE tweets.tweet_id = ?
"""



##############################
