-- tables
-- Table: followers
CREATE TABLE followers (
    follower_id bigint NOT NULL,
    followee_id bigint NOT NULL,
    CONSTRAINT followers_pk PRIMARY KEY (follower_id,followee_id)
);

-- Table: Mentions
CREATE TABLE mentions (
    tagged_users_id bigint NOT NULL,
    tweet_id bigint NOT NULL,
    CONSTRAINT mentions_pk PRIMARY KEY (tagged_users_id,tweet_id)
);

-- Table: Searches
CREATE TABLE searches (
    id bigint AUTO_INCREMENT,
    user_id bigint NOT NULL,
    last_date DATETIME NULL,
    count bigint NOT NULL,
    CONSTRAINT searches_pk PRIMARY KEY (id)
);

-- Table: Tweet_files
CREATE TABLE tweet_files (
    id bigint AUTO_INCREMENT,
    file_type text NOT NULL,
    file_url text NOT NULL,
    tweet_id bigint NOT NULL,
    CONSTRAINT tweet_files_pk PRIMARY KEY (id)
);

-- Table: Tweets
CREATE TABLE tweets (
    id bigint AUTO_INCREMENT,
    text text NOT NULL,
    date DATETIME NOT NULL,
    url text NOT NULL,
    user_id bigint NOT NULL,
    tweet_id bigint NOT NULL UNIQUE,
    CONSTRAINT tweets_pk PRIMARY KEY (id)
);

CREATE TABLE party (
	party_id bigint AUTO_INCREMENT,
	party_name varchar(100) NOT NULL UNIQUE,
	CONSTRAINT party_pk PRIMARY KEY (party_id)
);

    CREATE TABLE role (
	role_id bigint AUTO_INCREMENT,
	rol_name varchar(100) NOT NULL UNIQUE,
	CONSTRAINT role_pk PRIMARY KEY (role_id)
);

-- Table: Users
CREATE TABLE users (
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
    CONSTRAINT users_pk PRIMARY KEY (id)
);
-- foreign keys
-- Reference: Mentions_Tweets (table: Mentions)
ALTER TABLE mentions ADD CONSTRAINT mentions_tweets FOREIGN KEY mentions_tweets (tweet_id)
    REFERENCES tweets (id);

-- Reference: Mentions_Users (table: Mentions)
ALTER TABLE mentions ADD CONSTRAINT mentions_users FOREIGN KEY mentions_users (tagged_users_id)
    REFERENCES users (id);

-- Reference: Tweet_files_Tweets (table: Tweet_files)
ALTER TABLE tweet_files ADD CONSTRAINT tweet_files_tweets FOREIGN KEY tweet_files_tweets (tweets_id)
    REFERENCES tweets (id);

-- Reference: Tweets_Users (table: Tweets)
ALTER TABLE tweets ADD CONSTRAINT tweets_users FOREIGN KEY tweets_users (user_id)
    REFERENCES users (id);

-- Reference: Tweets_Users (table: Users)
ALTER TABLE users ADD CONSTRAINT users_role FOREIGN KEY users_role (role_id)
    REFERENCES role (role_id);

ALTER TABLE users ADD CONSTRAINT users_party FOREIGN KEY users_party (party_id)
    REFERENCES party (party_id);




---create index on screen_name in users table
CREATE INDEX screen_name_index ON  users(screen_name) USING BTREE;
---create index on full_name in users table
CREATE INDEX full_name_index ON  users(full_name) USING BTREE;

-- End of file.

