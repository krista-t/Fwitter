from bottle import post, request
import uuid
import globals
from datetime import datetime


##############################
def create_tweet(tweet, database = "database.sqlite"):
    status = {
        "success": False,
        "msg": "",
    }
    #inserted into db
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
@post("/tweet")
def _():
    #get info of user whois logged in
    image = request.files.get("image")
    now = datetime.now()
    time = now.strftime("%B-%d %H:%M:%S")

    try:
        db = globals._db_connect("database.sqlite")
        logged_user = db.execute( """SELECT *
        from users
        JOIN sessions  WHERE users.user_name  LIKE sessions.user_name""").fetchone()
        user_id = logged_user["user_id"]
        user_full_name = logged_user["user_full_name"]
        user_name = logged_user["user_name"]
        user_image = logged_user["user_image"]
        print("U"*10, logged_user)
        tweet = {
        "tweet_id": str(uuid.uuid4()),
        "tweet_text": request.forms.get("tweet_text"),
        "src": globals.validate_img(image),
        "tweet_created_at": time,
        "tweet_updated_at": time,
        "user_id": user_id,
        "user_image": user_image
        }
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        tweet = create_tweet(tweet)

        all_tweets = {
        "tweet_id": str(uuid.uuid4()),
        "tweet_text": request.forms.get("tweet_text"),
        "src": globals.validate_img(image),
        "user_name": user_name,
        "user_full_name": user_full_name,
        "tweet_created_at": time,
        "tweet_updated_at": time,
        "user_image": user_image
    }
    return all_tweets



