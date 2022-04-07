from bottle import post, request, response
import sqlite3
import uuid
import globals
import imghdr
import os
import datetime
#import json

##############################
def create_tweet(tweets, database = "database.sqlite"):
    status = {
        "success": False,
        "msg": "",
    }

    db = sqlite3.connect(database)
    try:
        db.execute(
            """INSERT INTO tweets
                VALUES(:tweet_id, :tweet_created_at, :tweet_text,
                :tweet_image,
                :tweet_updated_at,
                :tweet_user_id)""",
            tweets,
        )
        db.commit()
        status["success"] = True
        #status["msg"] = f"User {user['user_name']} succesfully created in database!"
        print(f"User {tweets['tweet_text']} succesfully created in database!")
    except Exception as ex:
        print(ex)
        status["msg"] = f"Unable to add user {tweets['tweet_id']} to database!"
        print(status["msg"])
    finally:
        db.close()
        return status


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
    try:
        db = globals._db_connect("database.sqlite")
        logged_user_id = db.execute( """SELECT  user_id
                                 from users
        INNER JOIN sessions WHERE users.user_name = sessions.user_name""").fetchall()
        response.content_type = "application/json"
        print("JJJJJJJJJJJJJJJJJJJ", logged_user_id)
        return logged_user_id
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        tweet = {
        "tweet_id": str(uuid.uuid4()),
        "tweet_created_at": datetime.datetime.now(),
        "tweet_text": request.forms.get("tweet_text"),
        "tweet_image": request.forms.get("image"),
        "tweet_updated_at": datetime.datetime.now(),
        "tweet_user_id": logged_user_id,
    }
        return tweet

    #status = validate_tweet(tweet)

    # if status["success"]:
    #     return create_user(user)
    # else:
    #     return status



