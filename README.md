MemSQL Pipelines Meetup
=======================

1. Run the MemSQL quickstart docker image with the included schema file.

```bash
docker run -d -v $(PWD)/schema.sql:/schema.sql -p 3306:3306 -p 9000:9000 --name=memsql memsql/quickstart
```

2. Open up the MemSQL Ops UI at http://localhost:9000

3. On the pipeline page create the first Pipeline:

```
    Kafka Hostname: public-kafka.memcompute.com
    Kafka Topic: tweets

    Database: twitter
    Table: tweets
```

4. On the pipeline page create another pipeline, but upload the included
   transform.py file and use the `tweet_links` table.

Example Queries
===============

**Top 10 most prolific users:**

```sql
SELECT username, COUNT(*) AS num_tweets
FROM tweets
GROUP BY username
ORDER BY num_tweets DESC
LIMIT 10
```

**Top 10 most retweeted tweets:**

```sql
SELECT username, body, retweet_count
FROM tweets
ORDER BY retweet_count DESC
LIMIT 10
```

**Top 10 most tweeted at users:**

```sql
SELECT ref_username, COUNT(*) AS num_references
FROM tweet_links
GROUP BY ref_username
ORDER BY num_references DESC
LIMIT 10
```

**Top 10 users by unique references:**

```sql
SELECT ref_username, COUNT(DISTINCT username) AS num_unique_references
FROM tweet_links
GROUP BY ref_username
ORDER BY num_unique_references DESC
LIMIT 10
```

**Top 10 pairs of users by mututal conversation:**

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
LIMIT 10
```
