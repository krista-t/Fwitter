from bottle import post, request, response
import sqlite3
import globals
import uuid
import jwt


def user_exists(user, database="database.sqlite"):
    """
    Check if a user exists in the database and validate the provided credentials.

    This function checks if the provided user_name exists in the database and verifies the provided user_password.
    It connects to the specified database and performs a query to find the user with the given user_name.

    Parameters:
        user (dict): A dictionary containing user information with the following keys:
                     - "user_name" (str): The username to check for existence in the database.
                     - "user_password" (str): The user's password to validate against the stored password.

        database (str): The filename of the SQLite database to connect to. Default is "database.sqlite".

    Returns:
        dict: A dictionary containing the result of the user validation. The dictionary will have the following keys:
                - "success" (bool): True if the user exists and the provided password is correct, False otherwise.
                - "msg" (str): A message indicating the status of the user validation.
                - "code" (str): The status code corresponding to the validation result.
                - "user" (str): The username of the validated user.
                - "image" (str): The user's profile image filename.

    Note:
        - The function executes the globals.USER_NAME_PASS_IMG_QUERY to fetch user information from the database.
        - If the user_name is not found in the database, the function returns a failure status with an appropriate message.
        - If the user_name exists in the database but the provided password is incorrect, the function returns a failure status.
        - If the user_name exists and the password is correct, the function returns a success status with the user information.
    """
    db = sqlite3.connect(database)
    status = {
        "success": False,
        "msg": "User does not exist!",
        "code": "status code",
        "user": "",
        "image": "",
    }
    if len(user["user_name"]) < 2:
        print(globals.ERROR["error_name_min"])
        status["msg"] = globals.ERROR["error_name_min"]
        status["code"] = globals._send(400, "bad request")
        return status
    # if user enters wrong password, but exists in DB
    if not user["user_password"]:
        print(globals.ERROR["error_password"])
        status["msg"] = globals.ERROR["error_password"]
        status["code"] = globals._send(400, "bad request")
        return status
    query_results = db.execute(
        globals.USER_NAME_PASS_IMG_QUERY, (user["user_name"],)
    ).fetchone()
    print("Q" * 10, query_results)
    if query_results:
        # index 1 is user_password
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


# create session for logged in users
def create_session(user):
    """
    Create a new session for the user and generate an authentication token.

    This function creates a new session for the provided user by generating a unique session_id using UUID4.
    It then inserts the session details (session_id, user_name, and user_password) into the 'sessions' table of the database.
    The function also generates an authentication token (JWT) containing user information and sets it as a cookie in the response.

    Parameters:
        user (dict): A dictionary containing user information with the following keys:
                     - "user_name" (str): The username of the user for whom the session is being created.
                     - "user_password" (str): The user's password.

    Returns:
        dict: A dictionary containing the session details. The dictionary will have the following keys:
                - "session_id" (str): A unique identifier for the session.
                - "user_name" (str): The username of the user associated with the session.
                - "user_password" (str): The user's password associated with the session.

    Note:
        - The function connects to the database using globals._db_connect("database.sqlite").
        - The function inserts the session details into the 'sessions' table using the provided user information.
        - It then generates a JWT token containing user information (name and session_id).
        - The JWT token is set as a cookie in the response with the name "token".
    """
    db = globals._db_connect("database.sqlite")
    try:
        sessions = {
            "session_id": str(uuid.uuid4()),
            "user_name": user["user_name"],
            "user_password": user["user_password"],
        }

        db.execute(
            """INSERT INTO sessions
                VALUES(:session_id, :user_name,
                :user_password)""",
            sessions,
        )
        db.commit()
        token = jwt.encode(
            {"name": user["user_name"], "session_id": sessions["session_id"]},
            "mysecret",
            algorithm="HS256",
        )
        response.set_cookie("token", token)
    except Exception as ex:
        print(ex)
        return globals._send(500, "server error")

    finally:
        db.close()
        return sessions


@post("/login")
def _():
    """
    Authenticate user login and create a session.

    This function handles the login process for users by extracting their login credentials (user_name and user_password)from the request form.
    It then calls the 'user_exists' function to check if the user exists in the database and if the
    provided credentials are correct. If the user exists and the credentials are valid, a new session is created using the'create_session' function, and a JWT token is set as a cookie in the response to authenticate the user.

    Returns:
        dict: A dictionary containing the login status and session details. The dictionary will have the following keys:
                - "success" (bool): True if the login is successful, False otherwise.
                - "msg" (str): A message indicating the status of the login process (e.g., "User does not exist!",
                               "Check your password!", "User validated!").
                - "code" (str): The status code for the response.
                - "user" (str): The username of the authenticated user (if login is successful).
                - "image" (str): The user's profile image associated with the authenticated user (if login is successful).

    Note:
        - The function uses the 'user_exists' function to check if the user exists and if the login credentials are valid.
        - If the login is successful (i.e., 'success' is True in the status dictionary returned by 'user_exists'),
          a new session is created using the 'create_session' function, and a JWT token is set as a cookie in the response.
        - The function connects to the database using globals._db_connect("database.sqlite").

    """
    user = {
        "user_name": request.forms.get("user_name"),
        "user_password": request.forms.get("user_password"),
    }
    status = user_exists(user)
    db = globals._db_connect("database.sqlite")
    try:
        # create sessions and set jwt token through function
        if status["success"] == True:
            create_session(user)
        else:
            status["success"] == False
    except Exception as ex:
        print(ex)
        status["code"] = globals._send(500, "server error")
    finally:
        db.close()
        return status
