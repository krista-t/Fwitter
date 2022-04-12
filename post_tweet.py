from bottle import post, request
import uuid
import globals
import imghdr
import os

##############################
def create_tweet(tweet, database = "database.sqlite"):
    status = {
        "success": False,
        "msg": "",
    }
    db = globals._db_connect(database)
    try:
        db.execute(
            """INSERT INTO tweets
                VALUES(:tweet_id,
                :tweet_text,
                :src,
                :user_name,
                :user_full_name)""",
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
    try:
        db = globals._db_connect("database.sqlite")
        logged_user = db.execute( """SELECT  *
        from users
        JOIN sessions  WHERE users.user_name  LIKE sessions.user_name""").fetchall()
        user_full_name = logged_user[0]["user_full_name"]
        user_name = logged_user[0]["user_name"]
        print("U"*10, logged_user[0]["user_name"])

    except Exception as ex:
        print(ex)
    finally:
        db.close()
        tweet = {
        "tweet_id": str(uuid.uuid4()),
        "tweet_text": request.forms.get("tweet_text"),
        "src": validate_img(image),
        "user_name": user_name,
        "user_full_name": user_full_name,
    }
        tweet = create_tweet(tweet)
    return tweet



