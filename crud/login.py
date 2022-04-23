from bottle import post, request, response
import sqlite3
import globals
import uuid
import jwt

#validate login and check if user exists, if not user is redirected to signup page
def user_exists(user, database = "database.sqlite"):
    db = sqlite3.connect(database)
    status = {
        "success": False,
        "msg": "User does not exist!",
        "code": "status code",
        "user": "",
        "image": ""
    }
    if len(user["user_name"]) < 2:
        print(globals.ERROR["error_name_min"])
        status["msg"] = globals.ERROR["error_name_min"]
        status["code"] = globals._send(400, "bad request")
        return status
    #if user enters wrong password, but exists in DB
    if not user["user_password"]:
        print(globals.ERROR["error_password"])
        status["msg"] = globals.ERROR["error_password"]
        status["code"] = globals._send(400, "bad request")
        return status
    query_results = db.execute(
        globals.USER_NAME_PASS_IMG_QUERY, (user["user_name"],)
    ).fetchone()
    print("Q"*10, query_results)
    if query_results:
        #index 1 is user_password
        if query_results[1] == user["user_password"]:
            status["success"] = True
            status["msg"] = "User validated!"
            status["user"] = user["user_name"]
            status["image"] = query_results[2]
            status["code"] = globals._send(200, "success")
            return status

        else:
            status["msg"] = "Check your password!"
            print(status["msg"])
            status["code"] = globals._send(400, "bad request")
            return status
    else:
        return status

###########################
#create session for logged in users
def create_session(user):
    db = globals._db_connect("database.sqlite")
    try:
        sessions = {
        "session_id":str(uuid.uuid4()),
        "user_name":user["user_name"],
        "user_password": user["user_password"]
    }

        db.execute(
            """INSERT INTO sessions
                VALUES(:session_id, :user_name,
                :user_password)""",
                sessions
        )
        db.commit()
        token = jwt.encode({
           "name":user["user_name"], "session_id": sessions["session_id"]
        }, "mysecret", algorithm="HS256")
        response.set_cookie("token",token)
    except Exception as ex:
        print(ex)
        return globals._send(500, "server error")

    finally:
        db.close()
        return sessions
##############################

@post("/login")
def _():
    user = {
        "user_name": request.forms.get("user_name"),
        "user_password": request.forms.get("user_password")
    }
    status = user_exists(user)
    db = globals._db_connect("database.sqlite")
    try:
    #create sessions and set jwt token through function
        if status["success"] == True:
            #function create_session
            create_session(user)
        else:
            status["success"] == False
    except Exception as ex:
        print(ex)
        status["code"] = globals._send(500, "server error")
    finally:
        db.close()
        return status


