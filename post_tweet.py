from bottle import post, request, response,view
import sqlite3
import uuid
import globals
import imghdr
import os
import datetime
import json

##############################
def create_tweet(tweet, database = "database.sqlite"):
    status = {
        "success": False,
        "msg": "",
    }

    db = sqlite3.connect(database)
    try:
        db.execute(
            """INSERT INTO tweets
                VALUES(:tweet_id,
                :tweet_text,
                :src,
                :user_id)""",
            tweet,
        )
        db.commit()
        status["success"] = True
        #status["msg"] = f"User {user['user_name']} succesfully created in database!"
        print(f"User {tweet['tweet_text']} succesfully created in database!")
    except Exception as ex:
        print(ex)
        status["msg"] = f"Unable to add user {tweet['tweet_id']} to database!"
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
# def _():
# #TODO:
#     # Validate
#     # Connect to the db
#     # response.status = 200
#     tweet_id = str(uuid.uuid4())
#     tweet_text = request.forms.get("tweet_text")
#     image = request.files.get("image")
#     tweet = {"id": tweet_id, "text": tweet_text, "src":validate_img(image) }
#     globals.TWEETS.append(tweet)
#     print("AAAAAAAAA", tweet)
#     return tweet

def _():
    #get id of user whois logged in
    image = request.files.get("image")
    try:
        db = globals._db_connect("database.sqlite")
        logged_user_id = db.execute( """SELECT user_id, user_full_name
                                 from users
        INNER JOIN sessions WHERE users.user_name = sessions.user_name""").fetchone()
        user_id = logged_user_id["user_id"]
        user_full_name = logged_user_id["user_full_name"]
        #print("A"*30,logged_user_id["user_id"])

    except Exception as ex:
        print(ex)
    finally:
        db.close()
        tweet = {
        "tweet_id": str(uuid.uuid4()),
        "tweet_text": request.forms.get("tweet_text"),
        "src": validate_img(image),
        "user_id": user_id
    }
        tweet = create_tweet(tweet)
        print(type(tweet))

    return tweet



