DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions(
session_id TEXT UNIQUE NOT NULL,
user_name TEXT NOT NULL,
user_password TEXT NOT NULL,
PRIMARY KEY(session_id)

)WITHOUT ROWID;

--REMEMBER TO RUN TE QUERY!

