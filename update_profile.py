from bottle import put, request, response
import globals
#############################
@put("/profile/<name_id>")
def _(name_id):


    #TODO: get values from the form, id is passed
    image = request.files.
    # image = {
    # "tweet_id": tweet_id,
    # "tweet_text": request.forms.get("tweet_text"),
    # "tweet_updated_at": now.strftime("%B-%d  %H:%M:%S")
    # #"src": validate_img(image),
    # }

    #TODO:validate, and status codes
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
        print("EXC"* 10, ex)
    finally:
        db.close()
        print("30"* 10, tweet)
        return tweet
