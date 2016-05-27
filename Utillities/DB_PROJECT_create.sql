CREATE SCHEMA `hoc_db` ;
-- tables
-- Table: Followers
CREATE TABLE Followers (
    follower_id bigint NOT NULL,
    followee_id bigint NOT NULL,
    CONSTRAINT Followers_pk PRIMARY KEY (follower_id,followee_id)
);

-- Table: Mentions
CREATE TABLE Mentions (
    tagged_users_id bigint NOT NULL,
    Tweet_id bigint NOT NULL,
    CONSTRAINT Mentions_pk PRIMARY KEY (tagged_users_id,Tweet_id)
);

-- Table: Searches
CREATE TABLE Searches (
    id bigint AUTO_INCREMENT,
    user_id1 bigint NOT NULL,
    user_id2 bigint NOT NULL,
    last_date DATETIME NULL,
    count bigint NOT NULL,
    CONSTRAINT Searches_pk PRIMARY KEY (id)
);

-- Table: Tweet_files
CREATE TABLE Tweet_files (
    id bigint AUTO_INCREMENT,
    file_type text NOT NULL,
    file_url text NOT NULL,
    Tweets_id bigint NOT NULL,
    CONSTRAINT Tweet_files_pk PRIMARY KEY (id)
);

-- Table: Tweets
CREATE TABLE Tweets (
    id bigint AUTO_INCREMENT,
    text text NOT NULL,
    date DATETIME NOT NULL,
    url text NOT NULL,
    User_id bigint NOT NULL,
    tweet_id bigint NOT NULL UNIQUE,
    CONSTRAINT Tweets_pk PRIMARY KEY (id)
);

CREATE TABLE Party (
	party_id bigint AUTO_INCREMENT,
	party_name varchar(100) NOT NULL UNIQUE,
	CONSTRAINT Party_pk PRIMARY KEY (party_id)
);

    CREATE TABLE Role (
	role_id bigint AUTO_INCREMENT,
	rol_name varchar(100) NOT NULL UNIQUE,
	CONSTRAINT Role_pk PRIMARY KEY (role_id)
);

-- Table: Users
CREATE TABLE Users (
    id bigint AUTO_INCREMENT,
    full_name varchar(200) NOT NULL,
    screen_name varchar(200) NOT NULL,
    description text NOT NULL,
    location varchar(100) NOT NULL,
    followers_count bigint NOT NULL,
    friends_count bigint NOT NULL,
    twitter_id bigint NOT NULL UNIQUE,
    profile_picture_url varchar(200) NULL,
    role_id bigint NOT NULL,
	party_id bigint NOT NULL,
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

-- Reference: Tweets_Users (table: Users)
ALTER TABLE Users ADD CONSTRAINT Users_Role FOREIGN KEY Users_Role (role_id)
    REFERENCES Role (role_id);

ALTER TABLE Users ADD CONSTRAINT Users_Party FOREIGN KEY Users_Party (party_id)
    REFERENCES Party (party_id);
-- End of file.

