from bottle import post, request
import uuid
import globals
import imghdr
import os

##############################
@post("/tweet")
def _():
    # TODO: JS issue?
    # Validate
    # Connect to the db
    # Insert the tweet in the tweets table
    # response.status = 200
    tweet_id = str(uuid.uuid4())
    tweet_text = request.forms.get("text")
    image = request.files.get("image")
    file_name, file_extension = os.path.splitext(image.filename)  # .png .jpeg .zip .mp4
    print(image.filename)  # sloth-unsplash.png
    if file_extension not in (".png", ".jpeg", ".jpg"):
        return "image not allowed"
    image_id = str(uuid.uuid4())
    # Create new image name
    tweet_img = f"{image_id}{file_extension}"
    print("#########", tweet_img)  # 23cf4153-c03a-4fe1-b2ca-7fbb9b973798.png
    # Save the image
    image.save(f"img/{tweet_img}")
    print("AAAAAAA", f"img/{tweet_img}")
    imghdr_extension = imghdr.what(f"img/{tweet_img}")
    print(f".{imghdr_extension}")  # .jpeg
    if file_extension != f".{imghdr_extension}":
        print("it is not an image format")
        os.remove(f"img/{tweet_img}")
        return "It is not an image"

    tweet = {"id": tweet_id, "text": tweet_text, "src": tweet_img}
    globals.TWEETS.append(tweet)
    print("AAAAAAAAA", tweet)
    return tweet


##############################
