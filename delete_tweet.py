from bottle import delete, response
import sqlite3
import globals

##############################
@delete("/delete_tweet/<tweet_id>")
def _(tweet_id):
    #validate that the tweet_id is a valid UUID4
   if globals._is_uuid4(tweet_id):
    #tweet_id = "1620fb63-e466-4816-89e8-98ee5fd451fa"
    #1620fb63-e466-4816-89e8-98ee5fd451fa
    db = sqlite3.connect("database.sqlite")
    try:
        deleted = db.execute(globals.DELETE_TWEET_QUERY, (tweet_id,)).fetchone()
        db.commit()
        print("D"*30,deleted)
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return deleted


    response.status = 204
    return "tweet not found"
