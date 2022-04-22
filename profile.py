
from bottle import get, view
import globals

@get("/<name_id>")
@view("profile")
def _(name_id):
    db = globals._db_connect("database.sqlite")
    try:
        name = db.execute(globals.GET_USER_QUERY, (name_id,)).fetchone()
        user = {
            "user_id": name["user_id"],
            "name": name["user_name"],
            "full_name": name["user_full_name"],
            "image": name["user_image"],
            "joined": name["user_created_at"]
        }

    except Exception as ex:
        print(ex)
        return globals._send(500, "something went wrong")
    try:
          #querry to fetch tweets of particular user
          user_tweets = name = db.execute(globals.GET_USER_TWEET_QUERY, (user["user_id"],)).fetchall()
          return user_tweets
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return dict(user=user,tweets = user_tweets)



