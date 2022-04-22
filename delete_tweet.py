from bottle import  delete, response
import sqlite3
import globals

##############################
@delete("/delete_tweet/<tweet_id>")
def _(tweet_id):
   print(tweet_id)
    #validate that the tweet_id is a valid UUID4
   if globals._is_uuid4(tweet_id):
    db = sqlite3.connect("database.sqlite")
    try:
        db.execute(globals.DELETE_TWEET_QUERY, (tweet_id,)).fetchone()
        db.commit()
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return "deleted"



