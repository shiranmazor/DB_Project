CREATE SCHEMA `hoc_db` ;
-- tables
-- Table: Followers
CREATE TABLE Followers (
    follower_id int NOT NULL,
    followee_id int NOT NULL,
    id int NOT NULL,
    CONSTRAINT Followers_pk PRIMARY KEY (id)
);

-- Table: Mentions
CREATE TABLE Mentions (
    id int NOT NULL,
    tagged_users_id int NOT NULL,
    Tweet_id int NOT NULL,
    CONSTRAINT Mentions_pk PRIMARY KEY (id)
);

-- Table: Searches
CREATE TABLE Searches (
    id int NOT NULL,
    user_id1 int NOT NULL,
    user_id2 int NOT NULL,
    last_date timestamp NOT NULL,
    count int NOT NULL,
    CONSTRAINT Searches_pk PRIMARY KEY (id)
);

-- Table: Tweets
CREATE TABLE Tweets (
    id int NOT NULL,
    text varchar(160) NOT NULL,
    date timestamp NOT NULL,
    url varchar(50) NOT NULL,
    User_id int NOT NULL,
    CONSTRAINT Tweets_pk PRIMARY KEY (id)
);

-- Table: Users
CREATE TABLE Users (
    id int NOT NULL,
    full_name varchar(50) NOT NULL,
    screen_name varchar(50) NOT NULL,
    description varchar(200) NOT NULL,
    location varchar(20) NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: Followers_Users (table: Followers)

-- Reference: Mentions_Tweets (table: Mentions)
ALTER TABLE Mentions ADD CONSTRAINT Mentions_Tweets FOREIGN KEY Mentions_Tweets (Tweet_id)
    REFERENCES Tweets (id);

-- Reference: Mentions_Users (table: Mentions)
ALTER TABLE Mentions ADD CONSTRAINT Mentions_Users FOREIGN KEY Mentions_Users (tagged_users_id)
    REFERENCES Users(id);

-- Reference: Tweets_Users (table: Tweets)
ALTER TABLE Tweets ADD CONSTRAINT Tweets_Users FOREIGN KEY Tweets_Users (User_id)
    REFERENCES Users (id);

-- End of file.

