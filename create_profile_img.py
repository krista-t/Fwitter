from bottle import put, request, get, response
import globals
import imghdr
import os
import uuid


def validate_img(image):
     #validate img format
    if image:
        file_name, file_extension = os.path.splitext(image.filename)  # .png .jpeg .zip .mp4
        if file_extension not in (".png", ".jpeg", ".jpg"):
         print("image not allowed")
        image_id = str(uuid.uuid4())
        # Create new image name
        img = f"{image_id}{file_extension}"
        print("#########", img)
        # Save the image
        image.save(f"img/{img}")
        imghdr_extension = imghdr.what(f"img/{img}")
        if file_extension != f".{imghdr_extension}":
            print(globals.ERROR["error_img"])
            os.remove(f"img/{img}")
            # return globals.ERROR["error_img"]
        else:
            return img
    #check if img exists
    elif not image:
        print("NO IMAGE")
        img = ""
        return img #None
#############################
@put("/<name_id>")
def _(name_id):
    print(name_id)
    #TODO: get values from the form, id is passed

    image = request.files.get("image")
    print(image)

    updated = {

     "user_image": validate_img(image),
     "user_name": name_id
     }

    # #TODO:validate, and status codes
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
        print("EXC"* 10, ex)
    finally:
        db.close()
        print(profile)

        return profile
