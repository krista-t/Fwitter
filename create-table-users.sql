DROP TABLE IF EXISTS users;

CREATE TABLE users(
user_id TEXT UNIQUE NOT NULL,
user_name TEXT NOT NULL,
user_full_name TEXT NOT NULL,
user_email  TEXT UNIQUE NOT NULL,
user_password TEXT NOT NULL,
PRIMARY KEY(user_id)

)WITHOUT ROWID;

CREATE INDEX idx_user_name ON users(user_name);
--REMEMBER TO RUN TE QUERY!