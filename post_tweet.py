from bottle import post, request
import uuid
import globals
from datetime import datetime


##############################
def create_tweet(tweet, database = "database.sqlite"):
    db = globals._db_connect(database)
    status = {
        "success": False,
        "msg": "",
        "code": "status code"
    }
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

##############################
@post("/tweet")
def _():
    image = request.files.get("image")
    now = datetime.now()
    time = now.strftime("%B-%d %H:%M:%S")
    id = str(uuid.uuid4())

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
        #validate img, uuid, tweet text
        tweet = {
        "tweet_id": globals._is_uuid4(id),
        "tweet_text": request.forms.get("tweet_text"),
        "src": globals.validate_img(image),
        "tweet_created_at": time,
        "tweet_updated_at": time,
        "user_id": user_id,
        "user_name": user_name,
        "user_full_name": user_full_name,
        "user_image": user_image
        }
    except Exception as ex:
        print(ex)
        ex = globals._send(500, "something went wrong")
        return ex
    finally:
        db.close()
        tweet = create_tweet(tweet)
        return tweet



