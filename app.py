from bottle import get, redirect, request, response, static_file, view,run
import json
import sqlite3
import jwt
import globals

##############################
import post_users_signup
import login
import post_tweet

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

    return dict(tabs=globals.TABS, trends = globals.TRENDS)

#################
@get("/signup")
@view("signup")
def _():
    return
#################


##############################
##this is just to make json, and to see sessions to test it in potman####
@get("/login")
def _():
    return
#     try:
#         db = globals._db_connect("database.sqlite")
#         sess_result = db.execute( """SELECT  user_id, user_email  from users
# INNER JOIN sessions  WHERE users.user_name = sessions.user_name""").fetchall()
#         response.content_type = "application/json"
#         print("JJJJJJJJJJJJJJJJJJJ", json.dumps(sess_result))
#         return json.dumps(sess_result)
#     except Exception as ex:
#         print(ex)
#     finally:
#         db.close()


##############################
@get("/logout")
def _():
    db = sqlite3.connect("database.sqlite")
    try:
        user_token = request.get_cookie("token")
    #TODO: encript decoded token
        decoded_token = jwt.decode(user_token,  "mysecret", algorithms = "HS256")
   #check if decoded_token["session_id"] is in sessions, and delete that row from sessions on logout
        db.execute(globals.DELETE_SESS_ROW_QUERY, (decoded_token["session_id"],)).fetchone()
        db.commit()
        print("LOGGING OOOOOOUT", decoded_token["session_id"])
        response.set_cookie("token", user_token, expires=0)
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return redirect("/")


##############################
try:
    import production
    application = default_app()  # don't import yet!
    print("***PRODUCTION***")
except Exception as ex:
    print("***Server running on development***")


run(host="127.0.0.1", port=3555, debug=True, reloader=True, server="paste")