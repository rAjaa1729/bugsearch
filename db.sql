DROP DATABASE IF EXISTS BugSearch;
CREATE DATABASE BugSearch;
USE BugSearch;

-- TABLE FOR USER
CREATE TABLE Users
(
    user_id INT NOT NULL AUTO_INCREMENT,
    passcode VARCHAR(200) NOT NULL,
    username VARCHAR(30) NOT NULL,
    email_id VARCHAR(40) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    profile_image_url VARCHAR(30),
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
    PRIMARY KEY (question_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (answer_id) REFERENCES Answers(answer_id)
);
ALTER TABLE Answers ADD FOREIGN KEY (question_id) REFERENCES Questions(question_id) ;


--
CREATE TABLE Comments
(
    comment_id INT NOT NULL AUTO_INCREMENT,
    body TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    post_type ENUM('question', 'answer') NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Questions(question_id), 
    FOREIGN KEY (post_id) REFERENCES Answers(answer_id) 
);

CREATE TABLE Votes
(
    vote_id INT NOT NULL AUTO_INCREMENT,
    vote_type ENUM('upvote', 'downvote') NOT NULL,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    post_type ENUM('question', 'answer') NOT NULL,
    PRIMARY KEY (vote_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Questions(question_id) ,
    FOREIGN KEY (post_id) REFERENCES Answers(answer_id) 
);

CREATE TABLE Tags
(
    tag_id INT NOT NULL AUTO_INCREMENT,
    tag_name VARCHAR(20) NOT NULL,
    about TEXT NOT NULL,
    PRIMARY KEY(tag_id)
);

CREATE TABLE Followertags
(
    fid INT AUTO_INCREMENT NOT NULL,
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(fid),
    FOREIGN KEY (follower_id) REFERENCES Users(user_id),
    FOREIGN KEY (following_id) REFERENCES Users(user_id)
);

CREATE TABLE Usertags
(
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (user_id,tag_id),
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Questiontags
(
    tag_id INT NOT NULL,
    question_id INT NOT NULL,
    PRIMARY KEY (question_id,tag_id),
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id),
    FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

CREATE TABLE Bookmarks
(
    Bookmark_id INT AUTO_INCREMENT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    post_type ENUM('question', 'answer') NOT NULL,
    PRIMARY KEY(Bookmark_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (post_id) REFERENCES Questions(question_id) ,
    FOREIGN KEY (post_id) REFERENCES Answers(answer_id) 
);

