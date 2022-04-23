from bottle import get, request, redirect,  view
import globals
import jwt

@get("/<name_id>")
@view("profile")
def _(name_id):
    user_token = request.get_cookie("token")
    decoded_token = jwt.decode(user_token,  "mysecret", algorithms = "HS256")
    print(decoded_token)
    logged_user = decoded_token["name"]

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
        if user_token:
            logged_user_img =  db.execute(globals.GET_LOGGED_USER_IMG_QUERY, (logged_user,)).fetchone()
            left_panel_img =  logged_user_img["user_image"]
        else:
            logged_user="guest"
            left_panel_img =  "blank.png"
            return redirect("/")
    except Exception as ex:
        print(ex)
        return globals._send(500, "something went wrong")
    try:
          #query to fetch tweets of particular user
          user_tweets = name = db.execute(globals.GET_USER_TWEET_QUERY, (user["user_id"],)).fetchall()
          return user_tweets
    except Exception as ex:
        print(ex)
    finally:
        db.close()
        return dict(user=user,tweets = user_tweets, logged_user=logged_user, trends = globals.TRENDS, logged_img = left_panel_img)



