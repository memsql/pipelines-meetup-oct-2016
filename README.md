MemSQL Pipelines Meetup
=======================

Setup with Docker
-----------------

* Run the MemSQL Quickstart Docker image with the included schema file.

```bash
docker run -d \
    -v $PWD/schema.sql:/schema.sql \
    -p 3306:3306 -p 9000:9000 \
    --name=memsql \
    memsql/quickstart
```

* Open up the MemSQL Ops UI at http://localhost:9000.

* Connect to the MemSQL database using `docker run --rm -it --link=memsql:memsql
  memsql/quickstart memsql-shell`.

Create Pipelines
----------------

* Navigate to "Data Sources" > "Pipelines">

* On the Pipelines page, create the first Pipeline:

```
    Kafka Hostname: public-kafka.memcompute.com
    Kafka Topic: tweets

    Database: twitter
    Table: tweets
```

* On the Pipelines page, create another pipeline, but upload the transform.py
  file included in this repo, and use the `tweet_links` table instead of the
  `tweets` table.

Example Queries
---------------

**Top 10 most prolific users:**

```sql
SELECT username, COUNT(*) AS num_tweets
FROM tweets
GROUP BY username
ORDER BY num_tweets DESC
LIMIT 10;
```

**Top 10 most retweeted tweets:**

```sql
SELECT username, body, MAX(retweet_count)
FROM tweets
GROUP BY body
ORDER BY retweet_count DESC
LIMIT 10;
```

**Top 10 most tweeted at users:**

```sql
SELECT ref_username, COUNT(*) AS num_references
FROM tweet_links
GROUP BY ref_username
ORDER BY num_references DESC
LIMIT 10;
```

**Random sample of tweets sent to a particular user**

```sql
SELECT body
FROM tweets, tweet_links
WHERE tweets.id = tweet_links.id
AND tweet_links.ref_username = "youtube"
LIMIT 10;
```

**Top 10 users by unique references:**

```sql
SELECT ref_username, COUNT(DISTINCT username) AS num_unique_references
FROM tweet_links
GROUP BY ref_username
ORDER BY num_unique_references DESC
LIMIT 10;
```

**Top 10 pairs of users by mutual conversation:**

```sql
SELECT edge, COUNT(*)
FROM (
    SELECT
        IF (
            username < ref_username,
            CONCAT(username, " -> ", ref_username),
            CONCAT(ref_username, " -> ", username)
        ) AS edge
    FROM tweet_links
) AS mapper
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```
