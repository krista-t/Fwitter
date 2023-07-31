from bottle import put, request, response
import globals


@put("/<name_id>")
def _(name_id):
    """
    Handle the PUT request for updating a user's profile image.

    This function is a route handler for the "/<name_id>" URL with the HTTP PUT method.
    It receives a name_id parameter from the URL and processes an uploaded image from the request.

    Parameters:
        name_id (str): The name_id extracted from the URL, representing the user's name or identifier.

    Returns:
        dict: A dictionary containing the updated user information, including the user's name_id and the validated image URL.

    Raises:
        bottle.HTTPResponse: If there is a server error (status code 500) during the database update or image validation.

    Note:
        - The function uses the globals.validate_img() function to validate and store the image.
        - It updates the user's profile image in the "users" table of the database.
        - The updated user information is returned as a JSON response.

    """

    image = request.files.get("image")
    updated = {"user_image": globals.validate_img(image), "user_name": name_id}

    db = globals._db_connect("database.sqlite")
    try:
        profile = db.execute(
            """
        UPDATE users
        SET user_image = :user_image
        WHERE
        user_name = :user_name
        """,
            updated,
        ).fetchone()
        response.content_type = "application/json"
        db.commit()
    except Exception as ex:
        ex = globals._send(500, "server error")
        return ex
    finally:
        db.close()
        return updated
