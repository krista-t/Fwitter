from bottle import put, response
import sqlite3
import globals

##############################
@put("/edit_tweet/<tweet_id>")
def _(tweet_id):
    #TODO: get values from the form, id is passed
    tweet = {
    "tweet_id": tweet_id,
    "tweet_text": "i am updated text 4",
    "tweet_image":"490865ca-cebd-4754-8136-95eeea454ea3.png"}

    #TODO:validate, and status codes
    db = sqlite3.connect("database.sqlite")
    try:
        edited = db.execute("""
    UPDATE tweets
    SET tweet_text = :tweet_text,
    tweet_image = :tweet_image
    WHERE
    tweet_id = :tweet_id
    """, tweet).fetchone()
        db.commit()
        print("E"*30,edited)

    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return edited

