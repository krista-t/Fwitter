from bottle import post, request
import sqlite3
import uuid
import re
import globals
from datetime import datetime


def validate_user(user, database="database.sqlite"):
    """
    Validate user information before registration.

    This function performs validation checks on the user information provided during registration.
    It checks the user's name, email, and password for specific criteria such as length, uniqueness,
    and proper email format. If any validation check fails, an error message with the corresponding
    status code is returned. Otherwise, the user information is considered valid, and a success status
    with a success code is returned.

    Parameters:
        user (dict): A dictionary containing the user information, including "user_name", "user_email",
                     and "user_password".
        database (str, optional): The path to the SQLite database file. Default is "database.sqlite".

    Returns:
        dict: A dictionary containing the validation status, message, and status code. The dictionary
              will have the following keys:
                - "success" (bool): True if the user information is valid, False otherwise.
                - "msg" (str): A message describing the validation status.
                - "code" (int): The HTTP status code associated with the validation status.

    Note:
        - The function uses regular expressions from the globals module to validate the email format.
        - It checks the user's name and email against the database to ensure uniqueness.
        - If any validation check fails, the function will return an error message and the corresponding status code.
    """
    status = {"success": False, "msg": "User not validated!", "code": "status code"}

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


def create_user(user, database="database.sqlite"):
    """
    Create a new user and add their information to the database.

    This function is responsible for inserting a new user record into the database with the provided user information.
    The user information should include "user_id", "user_name", "user_full_name", "user_email", "user_password",
    "user_image", and "user_created_at". After successfully inserting the new user, a success status with a success code
    is returned. In case of any error during the insertion process, an error message along with the corresponding status
    code is returned.

    Parameters:
        user (dict): A dictionary containing the user information, including "user_id", "user_name", "user_full_name",
                     "user_email", "user_password", "user_image", and "user_created_at".
        database (str, optional): The path to the SQLite database file. Default is "database.sqlite".

    Returns:
        dict: A dictionary containing the insertion status, message, and status code. The dictionary will have the following keys:
                - "success" (bool): True if the user was successfully added to the database, False otherwise.
                - "msg" (str): A message describing the insertion status.
                - "code" (int): The HTTP status code associated with the insertion status.

    Raises:
        bottle.HTTPResponse: If there is a server error (status code 500) during the database insertion.

    Note:
        - The function uses an SQLite database to store user information.
        - The "user_id" should be unique for each user to avoid conflicts.
        - The function returns a success status if the insertion is successful.
        - In case of any error, the function will return an error message and the corresponding status code.
    """
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


@post("/signup")
def _():
    """
    Handle the POST request for user signup.

    This function is a route handler for the "/signup" URL with the HTTP POST method.
    It receives user information from the request form and creates a new user with the provided details.
    The user information should include "user_full_name", "user_name", "user_email", and "user_password".
    Additionally, a unique "user_id" is generated using UUID to identify the new user.

    The function first validates the user information using the validate_user() function.
    If the validation is successful (i.e., the user information meets the required criteria),
    the new user is added to the database using the create_user() function, and a success status is returned.
    If any validation check fails, an error message with the corresponding status code is returned.

    Returns:
        dict: A dictionary containing the status of the user signup. The dictionary will have the following keys:
                - "success" (bool): True if the user signup is successful, False otherwise.
                - "msg" (str): A message describing the status of the user signup.
                - "code" (int): The HTTP status code associated with the user signup status.

    Note:
        - The function uses the validate_user() function to check the validity of the user information.
        - The function uses the create_user() function to add the new user to the database if the validation is successful.
    """
    now = datetime.now()
    time = now.strftime("%B-%d  %H:%M:%S")
    user = {
        "user_id": str(uuid.uuid4()),
        "user_full_name": request.forms.get("user_full_name"),
        "user_name": request.forms.get("user_name"),
        "user_email": request.forms.get("user_email"),
        "user_password": request.forms.get("user_password"),
        "user_image": "blank.png",
        "user_created_at": time,
    }

    status = validate_user(user)
    if status["success"]:
        return create_user(user)
    else:
        return status
