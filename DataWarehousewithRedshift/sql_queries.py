import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events (
    "artist" character varying(255),
    "auth" character varying(255),
    "firstName" character varying(255),
    "gender" character varying(5),
    "itemInSession" int,
    "lastName" character varying(255),
    "length" numeric(18,6),
    "level" character varying(255),
    "location" character varying(255),
    "method" character varying(25),
    "page" character varying(255),
    "registration" double precision,
    "sessionId" int,
    "song" character varying(255),
    "status" int,
    "ts" bigint,
    "userAgent" character varying(512),
    "userId" character varying(10)
)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    "num_songs" int NOT NULL,
    "artist_id" character varying(255),
    "artist_latitude" character varying(255),
    "artist_longitude" character varying(255),
    "artist_location" character varying(255),
    "artist_name" character varying(255),
    "song_id" character varying(255),
    "title" character varying(512),
    "duration" numeric(18,6),
    "year" int NOT NULL
);
""")

songplay_table_create = ("""
CREATE TABLE songplays (
    "songplay_id" int IDENTITY(0,1) PRIMARY KEY,
    "start_time" bigint NOT NULL,
    "user_id" character varying(10),
    "level" character varying(255) NOT NULL,
    "song_id" character varying(255) NOT NULL,
    "artist_id" character varying(255) NOT NULL,
    "session_id" int,
    "location" character varying(255),
    "user_agent" character varying(512)
);
""")

user_table_create = ("""
CREATE TABLE users (
    "user_id" character varying(10) NOT NULL PRIMARY KEY,
    "first_name" character varying(255),
    "last_name" character varying(255),
    "gender" character varying(5) NOT NULL,
    "level" character varying(255) NOT NULL
)
diststyle all;
""")

song_table_create = ("""
CREATE TABLE songs (
    "song_id" character varying(255) NOT NULL PRIMARY KEY sortkey,
    "title" character varying(512),
    "artist_id" character varying(255) NOT NULL,
    "year" int NOT NULL,
    "duration" numeric(18,6) NOT NULL
)
diststyle all;
""")


artist_table_create = ("""
CREATE TABLE artists (
    "artist_id" character varying(255) NOT NULL PRIMARY KEY sortkey,
    "name" character varying(255),
    "location" character varying(255),
    "latitude" character varying(255),
    "longitude" character varying(255)
)
diststyle all;
""")


time_table_create = ("""
CREATE TABLE time (
    "start_time" bigint NOT NULL  PRIMARY KEY,
    "hour" int NOT NULL,
    "day" int NOT NULL,
    "week" int NOT NULL,
    "month" int NOT NULL,
    "year" int NOT NULL,
    "weekday" character varying(255) NOT NULL
)
diststyle all;
""")


# STAGING TABLES

staging_events_copy = ("""copy staging_events from 's3://udacity-dend/log_data'
credentials 'aws_iam_role={}'
format json as 's3://udacity-dend/log_json_path.json'
region 'us-west-2'
""").format(config.get("IAM_ROLE","ARN"))

staging_songs_copy = ("""copy staging_songs from 's3://udacity-dend/song_data'
credentials 'aws_iam_role={}'
JSON 'auto'
region 'us-west-2'
""").format(config.get("IAM_ROLE","ARN"))

# FINAL TABLES

songplay_table_insert = ("""insert into songplays(start_time, user_id, level,
song_id, artist_id, session_id, location, user_agent)
(select distinct e.ts as start_time,e.userId,e.level,s.song_id,s.artist_id,e.sessionId,e.location,e.userAgent
from staging_events e, staging_songs s
where e.artist = s.artist_name and e.song = s.title and e.length = s.duration
and e.page = 'NextSong')
""")

user_table_insert = ("""insert into users
(select distinct e.userId,e.firstName,e.lastName,e.gender,e.level 
from staging_events e
where e.page = 'NextSong' and e.userId is not null
)
""")

song_table_insert = ("""insert into songs
(select distinct s.song_id,s.title,s.artist_id,s.year,s.duration 
from staging_songs s)
""")

artist_table_insert = ("""insert into artists
(select distinct s.artist_id,s.artist_name,s.artist_location,s.artist_latitude,s.artist_longitude 
from staging_songs s)
""")

time_table_insert = ("""insert into time
select distinct e.ts as start_time,
DATEPART(hour, date_add('ms',e.ts,'1970-01-01')) AS hour,
DATEPART(day, date_add('ms',e.ts,'1970-01-01')) AS day,
DATEPART(week, date_add('ms',e.ts,'1970-01-01')) AS week,
DATEPART(month, date_add('ms',e.ts,'1970-01-01')) AS month,
DATEPART(year, date_add('ms',e.ts,'1970-01-01')) AS year,
DATEPART(weekday, date_add('ms',e.ts,'1970-01-01')) AS weekday
from staging_events e
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert,time_table_insert]
 