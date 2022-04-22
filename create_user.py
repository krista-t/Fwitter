from bottle import post, request
import sqlite3
import uuid
import re
import globals
from datetime import datetime


def validate_user(user, database = "database.sqlite"):
    #TODO: put code statuses here?
    status = {
        "success": False,
        "msg": "User not validated!",
        "code": "status code"
    }

    db = sqlite3.connect(database)
    if len(user["user_name"]) < 2:
        print(globals.ERROR["error_name_min"])
        status["msg"] = globals.ERROR["error_name_min"]
        status["code"] = globals._send(400, "bad request")
        return status
    if len(user["user_name"]) > 20:
        print(globals.ERROR["error_name_max"])
        status["msg"] = globals.ERROR["error_name_max"]
        status["code"] = globals._send(400, "bad request")
        return status
    if not user["user_email"]:
        print(globals.ERROR["error_email"])
        status["msg"] = globals.ERROR["error_email"]
        status["code"] = globals._send(400, "bad request")
        return status
    if not re.match(globals.REGEX_EMAIL, user["user_email"]):
        print(globals.ERROR["error_email_re"])
        status["msg"] = globals.ERROR["error_email_re"]
        status["code"] = globals._send(400, "bad request")
        return status
    if not user["user_password"]:
        print("No Password provided!!!")
        status["msg"] = "No Password provided!!!"
        status["code"] = globals._send(400, "bad request")
        return status
    if len(user["user_password"]) < 6:
        print(globals.ERROR["error_password_min"])
        status["msg"] = globals.ERROR["error_password_min"]
        status["code"] = globals._send(400, "bad request")
        return status
    if db.execute(globals.USER_NAME_QUERY, (user["user_name"],)).fetchone():
        print("User name already exists")
        status["msg"] = "User name already exists"
        status["code"] = globals._send(400, "bad request")
        return status
    if db.execute(globals.USER_EMAIL_QUERY, (user["user_email"],)).fetchone():
        print("User email already exists")
        status["msg"] = "User email already exists"
        status["code"] = globals._send(400, "bad request")
        return status
    else:
        status["success"] = True
        status["code"] = globals._send(200, "success")
        print("User validated!")
        return status


def create_user(user, database = "database.sqlite"):
    status = {
        "success": False,
        "msg": "",
    }

    db = sqlite3.connect(database)
    try:
        db.execute(
            """INSERT INTO users
                VALUES(:user_id, :user_name, :user_full_name,
                :user_email, :user_password, :user_image, :user_created_at)""",
            user,
        )
        db.commit()
        status["success"] = True
        status["code"] = globals._send(200, "success")
        print(f"User {user['user_name']} succesfully created in database!")
    except Exception as ex:
        print(ex)
        status["msg"] = f"Unable to add user {user['user_name']} to database!"
        print(status["msg"])
        status["code"] = globals._send(500, "something went wrong")
    finally:
        db.close()
        return status


##############################
@post("/signup")
def _():
    now = datetime.now()
    time = now.strftime("%B-%d  %H:%M:%S")
    user = {
        "user_id": str(uuid.uuid4()),
        "user_full_name": request.forms.get("user_full_name"),
        "user_name": request.forms.get("user_name"),
        "user_email": request.forms.get("user_email"),
        "user_password": request.forms.get("user_password"),
        "user_image": "blank.png",
        "user_created_at": time
    }

    status = validate_user(user)

    if status["success"]:
        return create_user(user)
    else:
        return status
