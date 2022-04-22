from bottle import put, request, response
import sqlite3
import globals
import imghdr
import os
import uuid
from datetime import datetime
##############################
# def validate_img(image):
#      #validate img format
#     if image:
#         file_name, file_extension = os.path.splitext(image.filename)  # .png .jpeg .zip .mp4
#         if file_extension not in (".png", ".jpeg", ".jpg"):
#             print("image not allowed")
#         image_id = str(uuid.uuid4())
#         # Create new image name
#         tweet_img = f"{image_id}{file_extension}"
#         print("#########", tweet_img)
#         # Save the image
#         image.save(f"img/{tweet_img}")
#         imghdr_extension = imghdr.what(f"img/{tweet_img}")
#         if file_extension != f".{imghdr_extension}":
#             print(globals.ERROR["error_img"])
#             os.remove(f"img/{tweet_img}")
#             #return globals.ERROR["error_img"]
#         else:
#             return tweet_img
#     #check if img exists
#     elif not image:
#         print("NO IMAGE")
#         tweet_img = ""
#         return tweet_img #None
##############################
@put("/edit_tweet/<tweet_id>")
def _(tweet_id):

   #validate that the tweet_id is a valid UUID4
   if globals._is_uuid4(tweet_id):
    #image = request.files.get("image")
    #tweet_image = globals.validate_img(image)
    now = datetime.now()
    time = now.strftime("%B-%d  %H:%M:%S")
    tweet = {
    "tweet_id": tweet_id,
    "tweet_text": request.forms.get("tweet_text"),
    "tweet_updated_at": time
    }
    db = globals._db_connect("database.sqlite")
    try:
        db.execute("""
        UPDATE tweets
        SET tweet_text = :tweet_text,
            tweet_updated_at = :tweet_updated_at
        WHERE
        tweet_id = :tweet_id
        """, tweet).fetchone()
        response.content_type = "application/json"
        db.commit()

    except Exception as ex:
        ex = globals._send(500, "server error")
        return ex
    finally:
        db.close()
        return tweet



