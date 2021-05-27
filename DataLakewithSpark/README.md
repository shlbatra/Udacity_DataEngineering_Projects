## Project Summary
The project involves building a Big Data ETL pipeline to load the data from song files in JSON format that contain metadata about a song and the artist of that song & log files that contain activity logs in JSON format to AWS DataLake in S3 using Spark jobs to scale up and speed up data processing in the following tables -

- Fact Tables
    - songplays - Records with NextSong
- Dimension Tables
    - users - details about users of the app
    - songs - details about the song & artist
    - artists - details about the artists
    - time - details about the timestamp of records in songplays

We have broken down the data into the Fact & Dimenional data tables to allow for dimensional modelling. This allows us to run Analytical queries with minimal number of joins to keep up with performance of queries & reduce the redundancy. We loop across all the JSON files across S3 buckets for songs & logs files, and process the data into S3 Buckets with the above tables using Spark jobs in output Parquet format. 

### Below functions used to load the staging, fact & dimensional tables -


- def create_spark_session()
- def process_song_data(spark, input_data, output_data)
- def process_log_data(spark, input_data, output_data)              
    
        
### Code to run to execute the scripts -

- First setup Amazon EMR Cluster with 1 Master node and 3 worker nodes on AWS using UI or AWS CLI command with Spark installed
- SCP the etl.py & dl.cfg files on the root user or hadoop file system of the Cluster
- Run the python job using Spark Submit job - /usr/bin/spark-submit --master yarn ./etl.py

### Project Steps

The project template includes three files:

- etl.py reads data from S3, processes that data using Spark, and writes them back to S3
- dl.cfgcontains your AWS credentials
- README.md provides discussion on process and decisions
- data folder has a set of test files for songs and logs
- TestScripts_PySpark include testing scripts to debug Spark code.
