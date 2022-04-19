from bottle import get, redirect, request, response,static_file, view,run
import globals
import json

#TODO:ask about this

@get("/profile/<name_id>")
@view("/")
def _(name_id):

    db = globals._db_connect("database.sqlite")
    try:
        name = db.execute(globals.GET_USER_QUERY, (name_id,)).fetchone()
        return json.dumps(name)
    except Exception as ex:
        print(ex)
        #TODO: querry to fetch tweets of particular user
    finally:
        db.close()
        profile = {
            "name": name["user_name"],
            "full_name": name["user_full_name"]

        }
        print("NAM"*10, profile["full_name"])
        return json.dumps(profile)


