from bottle import post, request
import uuid
import globals
import imghdr
import os

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
        print("#########", tweet_img)  # 23cf4153-c03a-4fe1-b2ca-7fbb9b973798.png
        # Save the image
        image.save(f"img/{tweet_img}")
        #print("AAAAAAA", f"img/{tweet_img}")
        imghdr_extension = imghdr.what(f"img/{tweet_img}")
        #print(f".{imghdr_extension}")  # .jpeg
        if file_extension != f".{imghdr_extension}":
            print(globals.ERROR["error_img"])
            os.remove(f"img/{tweet_img}")
            return globals.ERROR["error_img"]
        else:
            return tweet_img
    #check if img exists
    elif not image:
        return image == ""

##############################
@post("/tweet")
def _():
#TODO:
    # Validate
    # Connect to the db
    # response.status = 200
    tweet_id = str(uuid.uuid4())
    tweet_text = request.forms.get("tweet_text")
    image = request.files.get("image")
    tweet = {"id": tweet_id, "text": tweet_text, "src":validate_img(image) }
    globals.TWEETS.append(tweet)
    print("AAAAAAAAA", tweet)
    return tweet



