from bottle import put, request, response
import globals
from datetime import datetime


@put("/edit_tweet/<tweet_id>")
def _(tweet_id):
    """
    Handle the PUT request to edit a specific tweet.

    This function is a route handler for the "/edit_tweet/<tweet_id>" URL with the HTTP PUT method.
    It takes a tweet_id as a parameter, which is the unique identifier of the tweet to be edited.
    The tweet_id is validated to ensure it is a valid UUID4 before proceeding with the update.

    The function receives the updated tweet text from the request form and updates the corresponding tweet's information
    in the database. The tweet_text and tweet_updated_at fields are updated with the new values.

    Parameters:
        tweet_id (str): The unique identifier (UUID4) of the tweet to be edited.

    Returns:
        dict: A dictionary containing the updated tweet information. The dictionary will have the following keys:
                - "tweet_id" (str): The unique identifier (UUID4) of the edited tweet.
                - "tweet_text" (str): The updated content of the tweet.
                - "tweet_updated_at" (str): The timestamp when the tweet was last updated.

    Note:
        - The function uses the globals._is_uuid4() function to validate the tweet_id as a valid UUID4.
        - The function executes an SQL UPDATE query to modify the tweet_text and tweet_updated_at fields in the database.
        - If the tweet with the specified tweet_id is not found, the function will return None.

    Example Usage:
        # Assuming the tweet_id is a valid UUID4 and corresponds to an existing tweet,
        # and the tweet_text is provided in the request form, the function will return a dictionary
        # containing the updated tweet information.
        updated_tweet_info = _("<valid_tweet_id>")
        print(updated_tweet_info)
    """
    if globals._is_uuid4(tweet_id):
        now = datetime.now()
        time = now.strftime("%B-%d  %H:%M:%S")
        tweet = {
            "tweet_id": tweet_id,
            "tweet_text": request.forms.get("tweet_text"),
            "tweet_updated_at": time,
        }
        db = globals._db_connect("database.sqlite")
        try:
            db.execute(
                """
            UPDATE tweets
            SET tweet_text = :tweet_text,
                tweet_updated_at = :tweet_updated_at
            WHERE
            tweet_id = :tweet_id
            """,
                tweet,
            ).fetchone()
            response.content_type = "application/json"
            db.commit()

        except Exception as ex:
            ex = globals._send(500, "server error")
            return ex
        finally:
            db.close()
            return tweet
