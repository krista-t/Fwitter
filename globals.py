from bottle import response
import re
import sqlite3
import uuid
import imghdr
import os

TRENDS = [
  {"category": "Technology", "title": "github", "tweets_counter": "53K"},
  {"category": "Arts&culture", "title": "#photography", "tweets_counter": "40k"},
  {"category": "Politics . Trending", "title": "Ukraine", "tweets_counter": "101M"},
  {"category": "Trends", "title": "#caturday", "tweets_counter": "19k"},
  {"category": "Trending in US", "title": "Russia", "tweets_counter": "45k"},
  {"category": "Music", "title": "Spotify", "tweets_counter": "45k"},
]

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

##############################
def _is_uuid4(text=None):
  if not text: return None
  regex_uuid4 = "^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
  if not re.match(regex_uuid4, text) : return None
  print(f"{text} valid uuid")
  return text

##############################
def _validate_img(image):
     #validate img format
    if image:
        file_name, file_extension = os.path.splitext(image.filename)  # .png .jpeg .zip .mp4
        if file_extension not in (".png", ".jpeg", ".jpg"):
          print("image not allowed")
        image_id = str(uuid.uuid4())
        # Create new image name
        tweet_img = f"{image_id}{file_extension}"
        print("#########", tweet_img)
        # Save the image
        image.save(f"img/{tweet_img}")
        imghdr_extension = imghdr.what(f"img/{tweet_img}")
        if file_extension != f".{imghdr_extension}":
            print(globals.ERROR["error_img"])
            os.remove(f"img/{tweet_img}")
            return globals.ERROR["error_img"]
        else:
            return tweet_img
    #check if img exists
    elif not image:
        print("NO IMAGE")
        tweet_img = ""
        return tweet_img #None






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
    # "error_img": "Wrong image format, only png, jpg, jpeg allowed"
}

##############################
def _send(status = 400, error_message = "unknown error"):
  response.status = status
  print(status)
  return {status:error_message}

##############################
##DB QUERIES##
#singup queries
USER_NAME_QUERY = """
SELECT user_name FROM users where user_name = ?
"""
USER_EMAIL_QUERY = """
SELECT user_email FROM users where user_email = ?
"""
#login query
USER_NAME_PASS_IMG_QUERY = """
SELECT user_name, user_password, user_image FROM users where user_name = ?
"""
#delete session query
DELETE_SESS_ROW_QUERY = """
DELETE FROM sessions WHERE session_id = ?"""

#delete tweet query
DELETE_TWEET_QUERY = """
DELETE FROM tweets WHERE tweets.tweet_id = ?"""

#show tweet with specific id query
GET_TWEET_WITH_ID_QUERY = """
SELECT * FROM tweets WHERE tweets.tweet_id = ?
"""
#get profile
GET_USER_QUERY = """
SELECT user_id, user_name, user_full_name, user_image, user_created_at FROM users WHERE users.user_name = ?
"""
#get single user tweet
GET_USER_TWEET_QUERY = """
SELECT * FROM tweets WHERE tweets.user_id = ? ORDER by tweet_created_at DESC
"""

#get logged user img on the left panel
GET_LOGGED_USER_IMG_QUERY = """
SELECT * FROM users WHERE users.user_name = ?
"""

##############################
