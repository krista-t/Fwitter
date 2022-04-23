from bottle import put, request,response
import globals

#############################
@put("/<name_id>")
def _(name_id):
    print(name_id)
    image = request.files.get("image")
    print(image)
    #validate image
    updated = {
     "user_image": globals.validate_img(image),
     "user_name": name_id
     }

    db = globals._db_connect("database.sqlite")
    try:
        profile=  db.execute("""
        UPDATE users
        SET user_image = :user_image
        WHERE
        user_name = :user_name
        """, updated).fetchone()
        response.content_type = "application/json"
        db.commit()
    except Exception as ex:
        ex = globals._send(500, "server error")
        return ex
    finally:
        db.close()
        return updated
