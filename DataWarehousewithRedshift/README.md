## Project Summary
The project involves building an ETL pipeline to load the data from song files in JSON format that contain metadata about a song and the artist of that song & log files that contain activity logs in JSON format to AWS Redshift datawarehouse in the following tables -

- Staging Tables
    - staging_events
    - staging_songs 
- Fact Tables
    - songplays - Records with NextSong
- Dimension Tables
    - users - details about users of the app
    - songs - details about the song & artist
    - artists - details about the artists
    - time - details about the timestamp of records in songplays

We have broken down the data into the Fact & Dimenional data tables to allow for dimensional modelling. This allows us to run Analytical queries with minimal number of joins to keep up with performance of queries & reduce the redundancy. We loop across all the JSON files and load the data from the files into the staging tables. Once staging tables are loaded, we use those tables to load the Fact & Dimesnion Tables. 

### Below functions used to load the staging, fact & dimensional tables -


- def drop_tables(cur, conn)
- def create_tables(cur, conn)
- def load_staging_tables(cur, conn)
- def insert_tables(cur, conn)                
    
        
### Code to run to execute the scripts -

- python create_tables.py
- python etl.py

### Project Steps

#### Create Tables

- Write CREATE statements in sql_queries.py to create staging, fact & dimension tables.
- Write DROP statements in sql_queries.py to drop staging, fact & dimension tables if it exists.
- Write copy table queries to load the data from song & log json files to staging tables
- Write insert commands based on select from staging tables to load data to Fact & Dimension tables.
- Run TestSQL.ipynb to confirm the creation of your tables with the correct columns. 


#### Build ETL Pipeline
- Create Redshift cluster & provide the details of the Cluster in dwh.cfg file.
- Implement etl.py to load data from S3 to Staging tables in Redshift.
- Furthermore, load data from Staging table to Fact & Dimension (Analytical) tables on Redshift
- Delete RedShift Cluster when finished



