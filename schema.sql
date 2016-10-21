DROP DATABASE IF EXISTS example;
CREATE DATABASE example;
USE example;


CREATE TABLE tweets (
    id TEXT,
    ts TIMESTAMP,
    retweet_count INT,
    favorite_count INT,
    username TEXT,
    body TEXT,
    KEY(username) USING CLUSTERED COLUMNSTORE
);


CREATE PIPELINE twitter_pipeline AS
    LOAD DATA KAFKA "10.0.2.38:9092/tweets"
    INTO TABLE tweets
    FIELDS TERMINATED BY "\t"
    (id, ts, retweet_count, favorite_count, username, body);


ALTER PIPELINE twitter_pipeline SET OFFSETS LATEST;
START PIPELINE twitter_pipeline;


CREATE TABLE tweet_links (
    a TEXT,
    b TEXT,
    KEY(a) USING CLUSTERED COLUMNSTORE
);


CREATE PIPELINE links_pipeline AS
    LOAD DATA KAFKA "10.0.2.38:9092/tweets"
    WITH TRANSFORM ("file:///home/admin/transform.py", "", "")
    INTO TABLE tweet_links
    FIELDS TERMINATED BY "\t"
    (a, b);


ALTER PIPELINE links_pipeline SET OFFSETS LATEST;
START PIPELINE links_pipeline;
