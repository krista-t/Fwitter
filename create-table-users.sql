DROP TABLE IF EXISTS users;

CREATE TABLE users(
user_id TEXT UNIQUE NOT NULL,
user_name TEXT NOT NULL,
user_full_name TEXT NOT NULL,
user_email TEXT UNIQUE NOT NULL,
user_password TEXT NOT NULL,
user_image TEXT,
user_created_at TEXT NOT NULL,
PRIMARY KEY(user_id)

)WITHOUT ROWID;

--REMEMBER TO RUN TE QUERY!