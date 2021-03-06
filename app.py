from bottle import get, redirect, request, response, static_file, view, run
import sqlite3
import jwt
import globals
import random
import json

##############################
from crud import create_user
from crud import post_tweet
from crud import delete_tweet
from crud import edit_tweet
from crud import login
from crud import create_profile_img
from crud import profile

##############################
@get("/app.css")
def _():
    return static_file("app.css", root=".")

##############################
@get("/js/script.js")
def _():
    return static_file("/js/script.js", root=".")

##############################
@get("/js/profile.js")
def _():
    return static_file("/js/profile.js", root=".")

##############################

@get("/js/validator.js")
def _():
    return static_file("/js/validator.js", root=".")

##############################
@get("/img/<image>")
def _(image):
    return static_file(image, root="./img")

##############################
@get("/")
@view("index")
def _():

    user_token = request.get_cookie("token")
    try:
        db = globals._db_connect("database.sqlite")
        tweets = db.execute("""SELECT * FROM tweets
                               JOIN users WHERE users.user_id
                                LIKE tweets.user_id
                                ORDER by tweet_created_at
                                DESC
                                """).fetchall()


        #check if user is logged in
        if user_token:
            decoded_token = jwt.decode(user_token,  "mysecret", algorithms = "HS256")
            logged_user = decoded_token["name"]
            print("TOKEN"*3, f"User {logged_user} is logged in")
            logged_user_img =  db.execute(globals.GET_LOGGED_USER_IMG_QUERY, (logged_user,)).fetchone()
            left_panel_img =  logged_user_img["user_image"]

        else:
            print("NOT TOKEN"*3, "Not logged in")
            logged_user="guest"
            left_panel_img =  "blank.png"

        #TODO: change to USERS suggested user panel is random
        suggested_user = random.sample(tweets,k=4)
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return dict(tweets = tweets, logged_user=logged_user, trends = globals.TRENDS, logged_img = left_panel_img, suggested_user = suggested_user)

#################
@get("/signup")
@view("signup")
def _():
    return

#################
@get("/login")
@view("login")
def _():
    return

##################
@get("/logout")
def _():
    db = sqlite3.connect("database.sqlite")
    try:
        user_token = request.get_cookie("token")
        decoded_token = jwt.decode(user_token,  "mysecret", algorithms = "HS256")
   #check if token id in sessions, and delete that row from sessions on logout
        db.execute(globals.DELETE_SESS_ROW_QUERY, (decoded_token["session_id"],)).fetchone()
        db.commit()
        response.set_cookie("token", user_token, expires=0)
    except Exception as ex:
        print(ex)
        return globals._send(500, "server_error")
    finally:
        db.close()
        return redirect("/")
##############################

try:
    import production
    application = default_app()
    print("***PRODUCTION***")
except Exception as ex:
    print("***Server running on development***")
    run(host="127.0.0.1", port=3999, debug=True, reloader=True, server="paste")

##############################
