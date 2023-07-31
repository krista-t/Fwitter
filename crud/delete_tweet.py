from bottle import delete
import sqlite3
import globals


@delete("/delete_tweet/<tweet_id>")
def _(tweet_id):
    """
    Handle the DELETE request to delete a specific tweet.

    This function is a route handler for the "/delete_tweet/<tweet_id>" URL with the HTTP DELETE method.
    It takes a tweet_id as a parameter, which is the unique identifier of the tweet to be deleted.
    The tweet_id is validated to ensure it is a valid UUID4 before proceeding with the deletion.

    The function attempts to delete the tweet with the specified tweet_id from the database using the DELETE_TWEET_QUERY.
    If the tweet is successfully deleted, the function returns the deleted tweet information.
    Otherwise, if there is any error during the deletion process, an error message with the corresponding status code is returned.

    Parameters:
        tweet_id (str): The unique identifier (UUID4) of the tweet to be deleted.

    Returns:
        dict: A dictionary containing the status of the tweet deletion. The dictionary will have the following keys:
                - "tweet_id" (str): The unique identifier (UUID4) of the deleted tweet.
                - "user_id" (str): The unique identifier (UUID4) of the user who posted the deleted tweet.
                - "tweet_content" (str): The content of the deleted tweet.
                - "tweet_created_at" (str): The timestamp when the tweet was created.

    Note:
        - The function uses the globals._is_uuid4() function to validate the tweet_id as a valid UUID4.
        - The function executes the DELETE_TWEET_QUERY to remove the tweet from the database.
        - If the tweet with the specified tweet_id is not found, the function will return None.
    """
    # validate that the tweet_id is a valid UUID4
    if globals._is_uuid4(tweet_id):
        db = sqlite3.connect("database.sqlite")
    try:
        deleted = db.execute(globals.DELETE_TWEET_QUERY, (tweet_id,)).fetchone()
        db.commit()
    except Exception as ex:
        print(ex)
        ex = globals._send(200, "something went wrong")
        return ex
    finally:
        db.close()
        return deleted  # nothing
