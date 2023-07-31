from bottle import get, redirect, request, response, static_file, view, run
import sqlite3
import jwt
import globals
import random
import json

from crud import (
    create_user,
    post_tweet,
    delete_tweet,
    edit_tweet,
    login,
    profile,
    create_profile_img,
)

# from crud import post_tweet
# from crud import delete_tweet
# from crud import edit_tweet
# from crud import login
# from crud import create_profile_img
# from crud import profile


# get static files
@get("/app.css")
def _():
    return static_file("app.css", root=".")


@get("/js/script.js")
def _():
    return static_file("/js/script.js", root=".")


@get("/js/profile.js")
def _():
    return static_file("/js/profile.js", root=".")


@get("/js/validator.js")
def _():
    return static_file("/js/validator.js", root=".")


@get("/img/<image>")
def _(image):
    return static_file(image, root="./img")


# routes
@get("/")
@view("index")
def _():
    """
    View function for handling the root URL ("/").

    This function fetches tweets from the database, along with user information, and prepares data
    to be displayed in the index view. It checks if the user is logged in based on the presence of
    a valid user token. If the user is logged in, it retrieves the user's details and profile image.
    Otherwise, it sets the user as a guest with a default profile image.

    Returns:
        dict: A dictionary containing the following keys and values:
            - "tweets" (list of dicts): A list of dictionaries containing tweet data fetched from the database.
            - "logged_user" (str): The name of the logged-in user or "guest" if not logged in.
            - "trends" (list): A list of trending topics or keywords.
            - "logged_img" (str): The image URL of the logged-in user's profile or a default blank image.
            - "suggested_user" (list of dicts): A list of randomly selected tweets to display in the suggested user panel.

    Raises:
        Exception: If there is an error during database query execution.

    Note:
        - The function uses a random sampling algorithm to select tweets for the suggested user panel.
        - The function uses the globals module to access global variables.
    """
    user_token = request.get_cookie("token")
    try:
        db = globals._db_connect("database.sqlite")
        tweets = db.execute(
            """SELECT * FROM tweets
                               JOIN users WHERE users.user_id
                                LIKE tweets.user_id
                                ORDER by tweet_created_at
                                DESC
                                """
        ).fetchall()

        if user_token:
            decoded_token = jwt.decode(user_token, "mysecret", algorithms="HS256")
            logged_user = decoded_token["name"]
            print("Token valid", f"User {logged_user} is logged in")
            logged_user_img = db.execute(
                globals.GET_LOGGED_USER_IMG_QUERY, (logged_user,)
            ).fetchone()
            left_panel_img = logged_user_img["user_image"]

        else:
            print("Not logged in")
            logged_user = "guest"
            left_panel_img = "blank.png"

        suggested_user = random.sample(tweets, k=4)
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return dict(
            tweets=tweets,
            logged_user=logged_user,
            trends=globals.TRENDS,
            logged_img=left_panel_img,
            suggested_user=suggested_user,
        )


# signup route
@get("/signup")
@view("signup")
def _():
    return


# login route
@get("/login")
@view("login")
def _():
    return


# logout route
@get("/logout")
def _():
    """
    View function for handling the "/logout" URL.

    This function is responsible for logging out the user. It first retrieves the user's token from the request's cookies,decodes the token to obtain the user's session information.
    It then checks if the session ID from the token is present in the sessions database table and deletes the corresponding row on logout. After successful logout, it clears the token
    cookie to log the user out of the system.

    Returns:
        bottle.HTTPResponse: A redirect response to the root URL ("/") after successful logout.

    Raises:
        bottle.HTTPResponse: If there is a server error (status code 500) during the logout process.

    Note:
        - The function relies on external database queries defined in the "globals" module.
        - It also uses the "jwt" module to decode the user token.

    """
    db = sqlite3.connect("database.sqlite")
    try:
        user_token = request.get_cookie("token")
        decoded_token = jwt.decode(user_token, "mysecret", algorithms="HS256")
        print("TOKEN IS", decoded_token["name"])
        # check if token id in sessions, and delete that row from sessions on logout
        db.execute(
            globals.DELETE_SESS_ROW_QUERY, (decoded_token["session_id"],)
        ).fetchone()
        db.commit()
        print("LOGGING OUT", decoded_token["session_id"])
        response.set_cookie("token", user_token, expires=0)
    except Exception as ex:
        print(ex)
        return globals._send(500, "server_error")
    finally:
        db.close()
        return redirect("/")


try:
    import production

    application = default_app()
    print("***PRODUCTION***")
except Exception as ex:
    print("***Server running on development***")
    run(host="127.0.0.1", port=3999, debug=True, reloader=True, server="paste")
