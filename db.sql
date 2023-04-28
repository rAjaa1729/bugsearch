DROP DATABASE IF EXISTS BugSearch;
CREATE DATABASE BugSearch;
USE BugSearch;

-- TABLE FOR USER
CREATE TABLE Users
(
    user_id INT NOT NULL AUTO_INCREMENT,
    passcode VARCHAR(200) NOT NULL ,
    username VARCHAR(30) NOT NULL UNIQUE,
    email_id VARCHAR(40) NOT NULL UNIQUE,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    profile_image_url VARCHAR(150),
    reputation INT NOT NULL DEFAULT 0,
    about TEXT,
    badge ENUM('bronze', 'silver', 'gold') NOT NULL DEFAULT 'bronze',
    nfollowers INT NOT NULL DEFAULT 0,
    nfollowing INT NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id)
);

-- TABLE FOR Answers
CREATE TABLE Answers
(
    answer_id INT NOT NULL AUTO_INCREMENT,
    body TEXT NOT NULL,
    question_id INT NOT NULL,
    user_id INT NOT NULL,
    score INT DEFAULT 0,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comment_count INT NOT NULL DEFAULT 0,
    upvotes INT NOT NULL DEFAULT 0,
    downvotes INT NOT NULL DEFAULT 0,
    PRIMARY KEY (answer_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) 
);

-- table for questions
CREATE TABLE Questions
(
    question_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100),
    body TEXT NOT NULL,
    answer_id INT ,
    user_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comment_count INT NOT NULL DEFAULT 0,
    answer_count INT NOT NULL DEFAULT 0,
    upvotes INT NOT NULL DEFAULT 0,
    downvotes INT NOT NULL DEFAULT 0,
    FULLTEXT(title,body),
    PRIMARY KEY (question_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (answer_id) REFERENCES Answers(answer_id)
);

ALTER TABLE Answers ADD FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE;

CREATE TABLE Answer_comments
(
    answer_comment_id INT NOT NULL AUTO_INCREMENT,
    body TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    answer_id INT NOT NULL,
    PRIMARY KEY (answer_comment_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (answer_id) REFERENCES Answers(answer_id) ON DELETE CASCADE
);


CREATE TABLE Question_comments
(
    question_comment_id INT NOT NULL AUTO_INCREMENT,
    body TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    PRIMARY KEY (question_comment_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE
);

-- insert into questions (title,body,user_id) values("raja","hi raja",1)

CREATE TABLE Answer_votes
(
    vote_type ENUM('upvote', 'downvote','neutral') NOT NULL DEFAULT 'neutral',
    answer_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (answer_id,user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (answer_id) REFERENCES Answers(answer_id) ON DELETE CASCADE
);

CREATE TABLE Question_votes
(
    vote_type ENUM('upvote', 'downvote','neutral') NOT NULL DEFAULT 'neutral',
    question_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (question_id,user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE
);

CREATE TABLE Tags
(
    tag_id INT NOT NULL AUTO_INCREMENT,
    tag_name VARCHAR(50) NOT NULL UNIQUE,
    about TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(tag_id)
);

-- following denotes user_id
-- follower denote which is following user_id

CREATE TABLE Followertags
(
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(follower_id,following_id),
    FOREIGN KEY (follower_id) REFERENCES Users(user_id),
    FOREIGN KEY (following_id) REFERENCES Users(user_id)
);

CREATE TABLE Usertags
(
    tag_name VARCHAR(50) NOT NULL ,
    user_id INT NOT NULL ,
    PRIMARY KEY (user_id,tag_name),
    FOREIGN KEY (tag_name) REFERENCES Tags(tag_name),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


CREATE TABLE Questiontags
(
    tag_name VARCHAR(50) NOT NULL ,
    question_id INT NOT NULL,
    PRIMARY KEY (question_id,tag_name),
    FOREIGN KEY (tag_name) REFERENCES Tags(tag_name),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE
);

CREATE TABLE Answer_bookmarks
(
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    answer_id INT NOT NULL,
    PRIMARY KEY(answer_id,user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (answer_id) REFERENCES Answers(answer_id) ON DELETE CASCADE
);

CREATE TABLE Question_bookmarks
(
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    PRIMARY KEY(question_id,user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id) ON DELETE CASCADE
);

-- insert into question_comments (question_id,body,user_id) values(1,"hi raja",1);


