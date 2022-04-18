from bottle import post, request
import uuid
import globals
import imghdr
import os
from datetime import datetime


##############################
def create_tweet(tweet, database = "database.sqlite"):
    status = {
        "success": False,
        "msg": "",
    }
    #INSERED USER ID BY JOIN
    db = globals._db_connect(database)
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
    except Exception as ex:
        print(ex)
        status["msg"] = f"Unable to add tweet {tweet['tweet_id']} to database!"
        print(status["msg"])
    finally:
        db.close()
        #check this
        return tweet

##############################
def validate_img(image):
     #validate img format
    if image:
        file_name, file_extension = os.path.splitext(image.filename)  # .png .jpeg .zip .mp4
        if file_extension not in (".png", ".jpeg", ".jpg"):
            print("image not allowed")
        image_id = str(uuid.uuid4())
        # Create new image name
        tweet_img = f"{image_id}{file_extension}"
        print("#########", tweet_img)
        # Save the image
        image.save(f"img/{tweet_img}")
        imghdr_extension = imghdr.what(f"img/{tweet_img}")
        if file_extension != f".{imghdr_extension}":
            print(globals.ERROR["error_img"])
            os.remove(f"img/{tweet_img}")
            return globals.ERROR["error_img"]
        else:
            return tweet_img
    #check if img exists
    elif not image:
        print("NO IMAGE")
        tweet_img = ""
        return tweet_img #None

##############################
@post("/tweet")
def _():
    #get info of user whois logged in
    image = request.files.get("image")
    now = datetime.now()

    try:
        db = globals._db_connect("database.sqlite")
        logged_user = db.execute( """SELECT *
        from users
        JOIN sessions  WHERE users.user_name  LIKE sessions.user_name""").fetchone()
        user_id = logged_user["user_id"]
        user_full_name = logged_user["user_full_name"]
        user_name = logged_user["user_name"]
        print("U"*10, logged_user["user_name"])
        tweet = {
        "tweet_id": str(uuid.uuid4()),
        "tweet_text": request.forms.get("tweet_text"),
        "src": validate_img(image),
        "tweet_created_at": now.strftime("%B-%d %H:%M:%S"),
        "tweet_updated_at": "",
        "user_id": user_id
        }
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        tweet = create_tweet(tweet)

        all_tweets = {
        "tweet_id": str(uuid.uuid4()),
        "tweet_text": request.forms.get("tweet_text"),
        "src": validate_img(image),
        "user_name": user_name,
        "user_full_name": user_full_name,
        "tweet_created_at": now.strftime("%B-%d %H:%M:%S"),
        "tweet_updated_at": ""
    }


    return all_tweets



