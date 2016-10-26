USE twitter;

CREATE PIPELINE twitter_pipeline AS
    LOAD DATA KAFKA "public-kafka.memcompute.com/tweets"
    INTO TABLE tweets
    FIELDS TERMINATED BY "\t"
    (id, ts, retweet_count, favorite_count, username, body);


ALTER PIPELINE twitter_pipeline SET OFFSETS LATEST;
START PIPELINE twitter_pipeline;


CREATE PIPELINE links_pipeline AS
    LOAD DATA KAFKA "public-kafka.memcompute.com/tweets"
    WITH TRANSFORM ("http://download.memsql.com/pipelines-twitter-demo/transform-meetup-oct25.py", "", "")
    INTO TABLE tweet_links
    FIELDS TERMINATED BY "\t"
    (username, ref_username);


ALTER PIPELINE links_pipeline SET OFFSETS LATEST;
START PIPELINE links_pipeline;
