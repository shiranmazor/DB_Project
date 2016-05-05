CREATE SCHEMA `hoc_db` ;
-- tables
-- Table: Followers
CREATE TABLE Followers (
    id bigint NOT NULL,
    follower_id bigint NOT NULL,
    followee_id bigint NOT NULL,
    CONSTRAINT Followers_pk PRIMARY KEY (id)
);

-- Table: Mentions
CREATE TABLE Mentions (
    id bigint NOT NULL,
    tagged_users_id bigint NOT NULL,
    Tweet_id bigint NOT NULL,
    CONSTRAINT Mentions_pk PRIMARY KEY (id)
);

-- Table: Searches
CREATE TABLE Searches (
    id bigint NOT NULL,
    user_id1 bigint NOT NULL,
    user_id2 bigint NOT NULL,
    last_date timestamp NULL,
    count bigint NOT NULL,
    CONSTRAINT Searches_pk PRIMARY KEY (id)
);

-- Table: Tweet_files
CREATE TABLE Tweet_files (
    id bigint NOT NULL,
    filename varchar(60) NOT NULL,
    file_url varchar(200) NOT NULL,
    Tweets_id bigint NOT NULL,
    CONSTRAINT Tweet_files_pk PRIMARY KEY (id)
);

-- Table: Tweets
CREATE TABLE Tweets (
    id bigint NOT NULL,
    text text NOT NULL,
    date date NOT NULL,
    url varchar(100) NOT NULL,
    User_id bigint NOT NULL,
    tweet_id bigint NOT NULL,
    CONSTRAINT Tweets_pk PRIMARY KEY (id)
);

-- Table: Users
CREATE TABLE Users (
    id bigint AUTO_INCREMENT,
    full_name varchar(100) NOT NULL,
    screen_name varchar(100) NOT NULL,
    description text NOT NULL,
    location varchar(100) NOT NULL,
    followers_count bigint NOT NULL,
    friends_count bigint NOT NULL,
    twitter_id bigint NOT NULL,
    profile_picture_url varchar(200) NULL,
    CONSTRAINT Users_pk PRIMARY KEY (id)
);
-- foreign keys
-- Reference: Mentions_Tweets (table: Mentions)
ALTER TABLE Mentions ADD CONSTRAINT Mentions_Tweets FOREIGN KEY Mentions_Tweets (Tweet_id)
    REFERENCES Tweets (id);

-- Reference: Mentions_Users (table: Mentions)
ALTER TABLE Mentions ADD CONSTRAINT Mentions_Users FOREIGN KEY Mentions_Users (tagged_users_id)
    REFERENCES Users (id);

-- Reference: Tweet_files_Tweets (table: Tweet_files)
ALTER TABLE Tweet_files ADD CONSTRAINT Tweet_files_Tweets FOREIGN KEY Tweet_files_Tweets (Tweets_id)
    REFERENCES Tweets (id);

-- Reference: Tweets_Users (table: Tweets)
ALTER TABLE Tweets ADD CONSTRAINT Tweets_Users FOREIGN KEY Tweets_Users (User_id)
    REFERENCES Users (id);

-- End of file.

