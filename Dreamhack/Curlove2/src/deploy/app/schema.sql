DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL,
    isAdmin INTEGER NOT NULL
);

INSERT INTO users VALUES('admin', '[**REDACTED**]','1');
