from bottle import response
import sqlite3



TRENDS = [
  {"category": "Music", "title": "We Won", "tweets_counter": "135K"},
  {"category": "Pop", "title": "Blue Ivy", "tweets_counter": "40k"},
  {"category": "Trending in US", "title": "Denim Day", "tweets_counter": "40k"},
  {"category": "Ukraine", "title": "Ukraine", "tweets_counter": "20k"},
  {"category": "Russia", "title": "Russia", "tweets_counter": "10k"},
]



PEOPLE = [
  {"src": "stephie.png", "name": "Stephie Jensen", "handle": "@sjensen"},
  {"src": "monk.jpg", "name": "Adrian Monk", "handle": "@detective :)"},
  {"src": "kevin.jpg", "name": "Kevin Hart", "handle": "@miniRock"}
]
TABS = [
    {"icon": "fas fa-home fa-fw", "title": "Home", "id": "home"},
    {"icon": "fas fa-hashtag fa-fw", "title": "Explore", "id": "explore"},
    {"icon": "far fa-bell fa-fw", "title": "Notifications", "id": "notifications"},
    {"icon": "far fa-envelope fa-fw", "title": "Messages", "id": "messages"},
    {"icon": "far fa-bookmark fa-fw", "title": "Bookmarks", "id": "bookmarks"},
    {"icon": "fas fa-clipboard-list fa-fw", "title": "Lists", "id": "lists"},
    {"icon": "far fa-user fa-fw", "title": "Profile", "id": "profile"},
    {"icon": "fas fa-ellipsis-h fa-fw", "title": "More", "id": "more"},
]

TWEETS = [
    {
        "src": "6.jpg",
        "user_first_name": "Barack",
        "user_last_name": "Obama",
        "user_name": "barackobama",
        "date": "Feb 20",
        "text": "The Ukrainian people need our help. If you’re looking for a way to make a difference, here are some organizations doing important work.",
        "image": "1.jpg",
    },
    {
        "src": "3.jpg",
        "user_first_name": "Elon",
        "user_last_name": "Musk",
        "user_name": "elonmusk",
        "date": "Mar 3",
        "text": "Richard Hunt is one of the greatest artists Chicago has ever produced, and I couldn’t be prouder that his “Book Bird” sculpture will live outside of the newest @ChiPubLibbranch at the Obama Presidential Center. I hope it inspires visitors for years to come.",
    },
    {
        "src": "2.jpg",
        "user_first_name": "Joe Biden",
        "user_last_name": "Biden",
        "user_name": "joebiden",
        "date": "Mar 7",
        "text": "Last year has been the best year for manufacturing jobs and trucking jobs since 1994.",
    },
]
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

COOKIE_SECRET = "SA6a$mLMH76%"
##############################


##############################
# create row in sqliteDB
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
# error signup/login server(image)
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
SELECT user_email FROM users where user_email=?
"""
#login query
USER_NAME_PASS_QUERY = """
SELECT user_name, user_password FROM users where user_name=?
"""
#delete session query
DELETE_SESS_ROW_QUERY = """
DELETE FROM sessions WHERE session_id= ?;"""
##############################
