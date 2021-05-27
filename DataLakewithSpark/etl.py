import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
import pyspark.sql.functions as F
from pyspark.sql import types as T
from datetime import datetime

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['KEYS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['KEYS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    
    """Description: This function can be used to create Spark Session 

    Returns:
    None"""
        
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    
    """Description: This function can be used to ingest the data from Song JSON files to Fact & Dimension Tables 

    Arguments:
        spark: spark object. 
        input_data: S3 folder with source files
        output_data: S3 folder with parquet output files

    Returns:
    None"""
        
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select("song_id", "title", "artist_id", "year", "duration").distinct()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year","artist_id").mode("overwrite").parquet(output_data+"songs.parquet")

    # extract columns to create artists table
    artists_table = df.select("artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude").distinct()
    
    # write artists table to parquet files
    artists_table.write.mode("overwrite").parquet(output_data+"artists.parquet")


def process_log_data(spark, input_data, output_data):
    
    """Description: This function can be used to ingest the data from Log JSON files to Fact & Dimension Tables 

    Arguments:
        spark: spark object. 
        input_data: S3 folder with source files
        output_data: S3 folder with parquet output files

    Returns:
    None"""
    
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users_table = df.select("userId", "firstName", "lastName", "gender", "level").distinct()
    
    # write users table to parquet files
    users_table.write.mode("overwrite").parquet(output_data+"users.parquet")

    # create timestamp column from original timestamp column
    get_timestamp = F.udf(lambda x: datetime.fromtimestamp( (x/1000.0) ), T.TimestampType())
    df = df.withColumn("timestamp",get_timestamp("ts"))
    
    # create datetime column from original timestamp column
    get_datetime = F.udf(lambda x: datetime.date(datetime.fromtimestamp( (x/1000.0) )), T.DateType())
    df = df.withColumn("datetimecolumn",get_datetime("ts"))
    
    # extract columns to create time table
    time_table = df.select("ts","timestamp","datetimecolumn").withColumn("hour",F.hour(F.col("timestamp")))\
           .withColumn("day",F.dayofyear(F.col("timestamp")))\
           .withColumn("week",F.weekofyear(F.col("timestamp")))\
           .withColumn("month",F.month(F.col("timestamp")))\
           .withColumn("year",F.year(F.col("timestamp")))\
           .withColumn('weekday', F.date_format(F.col("timestamp"), 'EEEE'))
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year","month").mode("overwrite").parquet(output_data+"time.parquet")

    # read in song data to use for songplays table
    song_df = spark.read.json('s3a://udacity-dend/song_data/*/*/*/*.json')
    
    
    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = df.join(song_df, (df.artist == song_df.artist_name)\
                                        & (df.song == song_df.title)\
                                        & (df.length == song_df.duration))\
                              .join(time_table,(df.ts == time_table.ts))\
                              .select(time_table.ts,"userId", "level", "song_id", 
                                      "artist_id", "sessionId", "location", "userAgent",time_table.year,"month")   
    
    songplays_table = songplays_table.withColumn("idx", F.monotonically_increasing_id())
    window = W.orderBy(F.col('idx'))
    songplays_table = songplays_table\
                  .withColumn("songplay_id",F.row_number().over(window))\
                  .select("songplay_id","ts","userId","level","song_id","artist_id","sessionId","location", "userAgent","year","month")
    
    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year","month").mode("overwrite")\
                                                     .parquet(output_data+"songplays.parquet")


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3://sahilfirstbuckets3/output/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)
    spark.stop()

if __name__ == "__main__":
    main()
