from bottle import get, request, redirect, view
import globals
import jwt


@get("/<name_id>")
@view("profile")
def _(name_id):
    """
    Display the profile page for a specific user.

    This function handles the GET request to display the profile page of a user identified by the given name_id.
    It first checks for the user token stored in the request cookies. If the token exists, it is decoded using the
    "mysecret" key and the HS256 algorithm to retrieve the name of the logged-in user. The database is then queried to fetch the user information (user_id, name, full_name, image, and joined timestamp) for the specified name_id.
    If the user token is valid, the logged-in user's image is also fetched from the database.

    Parameters:
        name_id (str): The unique ID or name of the user whose profile is to be displayed.

    Returns:
        dict: A dictionary containing the user profile information and a list of tweets posted by the user.
        The dictionary will have the following keys:
            - "user" (dict): A dictionary containing the following user profile information:
                - "user_id" (str): The unique ID of the user.
                - "name" (str): The username of the user.
                - "full_name" (str): The full name of the user.
                - "image" (str): The URL of the user's profile picture.
                - "joined" (str): The timestamp when the user joined (formatted as "%B-%d %H:%M:%S").
            - "tweets" (list): A list of dictionaries representing the tweets posted by the user. Each dictionary will
                contain the tweet information, such as tweet_id, tweet_text, src, tweet_created_at, and tweet_updated_at.
            - "logged_user" (str): The username of the logged-in user (if a valid token exists).
            - "trends" (list): A list of trending topics or hashtags.
            - "logged_img" (str): The URL of the logged-in user's profile picture (if a valid token exists).

    Note:
        - The function uses the 'name_id' parameter to query the 'users' table in the database and fetch the user
          profile information.
        - The function connects to the database using globals._db_connect("database.sqlite").
        - The function uses the GET_USER_TWEET_QUERY to fetch the tweets posted by the specified user from the 'tweets'
          table in the database.
    """
    user_token = request.get_cookie("token")
    user_token_bytes = user_token.encode("utf-8")
    decoded_token = jwt.decode(user_token_bytes, "mysecret", algorithms="HS256")
    print(decoded_token)
    logged_user = decoded_token["name"]
    db = globals._db_connect("database.sqlite")
    try:
        name = db.execute(globals.GET_USER_QUERY, (name_id,)).fetchone()
        user = {
            "user_id": name["user_id"],
            "name": name["user_name"],
            "full_name": name["user_full_name"],
            "image": name["user_image"],
            "joined": name["user_created_at"],
        }
        if user_token:
            logged_user_img = db.execute(
                globals.GET_LOGGED_USER_IMG_QUERY, (logged_user,)
            ).fetchone()
            left_panel_img = logged_user_img["user_image"]
        else:
            logged_user = "guest"
            left_panel_img = "blank.png"
            return redirect("/")
    except Exception as ex:
        print(ex)
        return globals._send(500, "something went wrong")
    try:
        # query to fetch tweets of particular user
        user_tweets = name = db.execute(
            globals.GET_USER_TWEET_QUERY, (user["user_id"],)
        ).fetchall()
        return user_tweets
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return dict(
            user=user,
            tweets=user_tweets,
            logged_user=logged_user,
            trends=globals.TRENDS,
            logged_img=left_panel_img,
        )
