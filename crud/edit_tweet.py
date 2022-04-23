from bottle import put, request, response
import globals
from datetime import datetime
##############################

@put("/edit_tweet/<tweet_id>")
def _(tweet_id):

   #validate that the tweet_id is a valid UUID4
   if globals._is_uuid4(tweet_id):
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



