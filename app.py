from bottle import get, redirect, request, response, static_file, view, run
import sqlite3
import jwt
import globals
import random

##############################
import create_user
import login
import post_tweet
import delete_tweet
import edit_tweet
import profile
import create_profile_img

##############################
@get("/app.css")
def _():
    return static_file("app.css", root=".")

##############################
@get("/JS/script.js")
def _():
    return static_file("js/script.js", root=".")

##############################
@get("/JS/validator.js")
def _():

    return static_file("js/validator.js", root=".")

##############################
@get("/img/<image>")
def _(image):
    return static_file(image, root="./img")

##############################
@get("/")
@view("index")
def _():
    user_token = request.get_cookie("token")
    db = globals._db_connect("database.sqlite")
    try:
        tweets = db.execute("""SELECT * FROM tweets
                               JOIN users WHERE users.user_id
                                LIKE tweets.user_id
                                ORDER by tweet_created_at
                                DESC
                                """).fetchall()
        print(tweets)
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

        #make dict for suggested user panel
        #suggested_user = random.sample(tweets,k=5)
    except Exception as ex:
        print(ex)
    finally:
        db.close()

    return dict(tweets=tweets, logged_user=logged_user, trends = globals.TRENDS, logged_img = left_panel_img)

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
        print("TOK"*10, decoded_token["name"])
   #check if token id in sessions, and delete that row from sessions on logout
        db.execute(globals.DELETE_SESS_ROW_QUERY, (decoded_token["session_id"],)).fetchone()
        db.commit()
        print("LOGGING OOOOOOUT", decoded_token["session_id"])
        response.set_cookie("token", user_token, expires=0)
    except Exception as ex:
        print(ex)
        return globals._send(500, "server_error")
    finally:
        db.close()
        return redirect("/")
##############################



##############################
try:
    import production
    application = default_app()  # don't import yet!
    print("***PRODUCTION***")
except Exception as ex:
    print("***Server running on development***")

##############################
run(host="127.0.0.1", port=3555, debug=True, reloader=True, server="paste")