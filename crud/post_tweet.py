from bottle import post, request
import uuid
import globals
from globals import ERROR
from datetime import datetime


def create_tweet(tweet, database="database.sqlite"):
    """
    Create a new tweet and add it to the database.

    This function takes a dictionary 'tweet' containing tweet information as input and inserts the tweet data into the 'tweets' table in the specified database. The 'tweet' dictionary should have the following keys:
        - "tweet_id" (str): The unique ID of the tweet.
        - "tweet_text" (str): The text content of the tweet.
        - "src" (str): The source of the tweet (e.g., image URL or video URL).
        - "tweet_created_at" (str): The timestamp when the tweet is created (formatted as "%B-%d  %H:%M:%S").
        - "tweet_updated_at" (str): The timestamp when the tweet is last updated (formatted as "%B-%d  %H:%M:%S").
        - "user_id" (str): The unique ID of the user who posted the tweet.

    Parameters:
        tweet (dict): A dictionary containing tweet information as described above.
        database (str, optional): The name of the database to connect to. Default is "database.sqlite".

    Returns:
        dict: A dictionary containing the status of the tweet creation. The dictionary will have the following keys:
            - "success" (bool): True if the tweet is created successfully, False otherwise.
            - "msg" (str): A message indicating the status of the tweet creation process (e.g., "Tweet text is too long!",
                           "Tweet created successfully!", "Unable to add tweet to database!").
            - "code" (str): The status code for the response.

    Note:
        - The function checks if the length of the tweet text is greater than 80 characters and returns an error
          status if it exceeds the limit.
        - If the tweet text is not provided ('tweet_text' key is empty) and 'src' is also not provided, an error status is returned.
        - The function connects to the database using globals._db_connect("database.sqlite").
        - If the tweet is created successfully, the function returns the 'tweet' dictionary with the inserted data.
    """
    db = globals._db_connect(database)
    status = {"success": False, "msg": "", "code": "status code"}
    if len(tweet["tweet_text"]) > 80:
        status["msg"] = globals.ERROR["error_tweet_text"]
        status["code"] = globals._send(400, "bad request")
        return status
    if not tweet["tweet_text"] and not tweet["src"]:
        status["msg"] = globals.ERROR["error_tweet_text"]
        status["code"] = globals._send(400, "bad request")
        return status
    try:
        db.execute(
            """INSERT INTO tweets
                VALUES(:tweet_id,
                :tweet_text,
                :src,
                :tweet_created_at,
                :tweet_updated_at,
                :user_id)
                """,
            tweet,
        )
        db.commit()
        status["success"] = True
        print(f"Tweet {tweet['tweet_text']} succesfully created in database!")
        status["code"] = globals._send(200, "success")
        return tweet
    except Exception as ex:
        print(ex)
        status["msg"] = f"Unable to add tweet {tweet['tweet_id']} to database!"
        print(status["msg"])
        status["code"] = globals._send(500, "something went wrong")
        return status
    finally:
        db.close()
        return tweet


@post("/tweet")
def _():
    """
    Create a new tweet and add it to the database.

    This function handles the POST request to create a new tweet. The tweet data is obtained from the request form,including the tweet text and an optional image file. The function generates a unique tweet ID using UUID, and the tweet creation timestamp is set to the current date and time. The logged-in user's information, such as user ID,full name, username, and user image, is retrieved from the database using the user session.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the tweet information. The dictionary will have the following keys:
            - "tweet_id" (str): The unique ID of the tweet.
            - "tweet_text" (str): The text content of the tweet.
            - "src" (str): The source of the tweet (e.g., image URL or video URL).
            - "tweet_created_at" (str): The timestamp when the tweet is created (formatted as "%B-%d %H:%M:%S").
            - "tweet_updated_at" (str): The timestamp when the tweet is last updated (formatted as "%B-%d %H:%M:%S").
            - "user_id" (str): The unique ID of the user who posted the tweet.
            - "user_name" (str): The username of the user who posted the tweet.
            - "user_full_name" (str): The full name of the user who posted the tweet.
            - "user_image" (str): The image URL of the user's profile picture.

    Note:
        - The function connects to the database using globals._db_connect("database.sqlite").
        - The function uses the create_tweet function to insert the tweet data into the 'tweets' table in the database.
          The create_tweet function is expected to return a dictionary containing the status of the tweet creation.
    """
    image = request.files.get("image")
    now = datetime.now()
    time = now.strftime("%B-%d %H:%M:%S")
    id = str(uuid.uuid4())

    try:
        db = globals._db_connect("database.sqlite")
        logged_user = db.execute(
            """SELECT *
        from users
        JOIN sessions  WHERE users.user_name  LIKE sessions.user_name"""
        ).fetchone()
        user_id = logged_user["user_id"]
        user_full_name = logged_user["user_full_name"]
        user_name = logged_user["user_name"]

        # if user image is not available, use empty string
        user_image = logged_user["user_image"]
        # validate img, uuid, tweet text
        if not user_image:
            user_image = globals.DEFAULT["default_user_image"]

        tweet = {
            "tweet_id": globals._is_uuid4(id),
            "tweet_text": request.forms.get("tweet_text"),
            # if src is not available, use empty string
            "src": globals.validate_img(image) if image else "",
            "tweet_created_at": time,
            "tweet_updated_at": time,
            "user_id": user_id,
            "user_name": user_name,
            "user_full_name": user_full_name,
            "user_image": user_image,
        }
        tweet = create_tweet(tweet)
    except Exception as ex:
        print(ex)
        ex = globals._send(500, "something went wrong")
        return ex
    finally:
        db.close()

    return tweet
