CREATE TABLE users (
    username VARCHAR2(50),
    password VARCHAR2(50)
);

INSERT INTO users (username, password) VALUES ('admin', 'admin123');
INSERT INTO users (username, password) VALUES ('user1', 'pass123');
INSERT INTO users (username, password) VALUES ('guest', 'guestpass');

COMMIT;