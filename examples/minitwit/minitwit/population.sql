INSERT INTO user (username, email, pw_hash)
VALUES ('swati', 'swati@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (username, email, pw_hash)
VALUES ('sachin', 'sachin@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (username, email, pw_hash)
VALUES ('satish', 'satish@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (username, email, pw_hash)
VALUES ('saket', 'saket@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (username, email, pw_hash)
VALUES ('disu', 'disu@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (username, email, pw_hash)
VALUES ('nani', 'nani@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO follower
VALUES (1, 2);

INSERT INTO follower
VALUES (1, 3);

INSERT INTO follower
VALUES (2, 3);

INSERT INTO follower
VALUES (4, 3);

INSERT INTO follower
VALUES (5, 1);

INSERT INTO follower
VALUES (3, 2);

INSERT INTO message (author_id, text, pub_date)
VALUES (1, 'Hey everyone!', 100); 

INSERT INTO message (author_id, text, pub_date)
VALUES (2, 'Hey! Goodmorning!', 100);

INSERT INTO message (author_id, text, pub_date)
VALUES (5, 'Have a great day guys!', 100); 

