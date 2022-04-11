from bottle import put, request
import sqlite3
import globals
import imghdr
import os
import uuid
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
@put("/edit_tweet/<tweet_id>")
def _(tweet_id):
    #TODO: get values from the form, id is passed
    image = request.files.get("image")
    tweet = {
    "tweet_id": tweet_id,
    "tweet_text": request.forms.get("tweet_text"),
    "src": validate_img(image),
    }

    #TODO:validate, and status codes
    db = globals._db_connect("database.sqlite")
    try:
        db.execute("""
        UPDATE tweets
        SET tweet_text = :tweet_text,
        tweet_image = :src
        WHERE
        tweet_id = :tweet_id
        """, tweet).fetchone()
        db.commit()
    except Exception as ex:
        print("30"* 10, ex)
    finally:
        db.close()
        print("30"* 10, tweet)
        return tweet



