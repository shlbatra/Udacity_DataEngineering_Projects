## Project Summary
The project involves building an ETL pipeline to load the data from 30 JSON files to Postgres database in the following tables -

- songplays
- users
- songs
- artists
- time

We have broken down the data into the above mentioned tables to keep the data normalized & ACID. We loop across all the 30 files and load the data from the files into the tables one by one. 

### Below functions used to load the file -

- def process_log_file(cur, filepath)
- def process_song_file(cur, filepath)                
- def process_data(cur, conn, filepath, func)
    
        
### Code to run to execute the scripts -

- python create_tables.py
- python etl.py

### Project Steps

#### Create Tables

- Write CREATE statements in sql_queries.py to create each table.
- Write DROP statements in sql_queries.py to drop each table if it exists.
- Run create_tables.py to create your database and tables.
- Run test.ipynb to confirm the creation of your tables with the correct columns. Make sure to click "Restart kernel" to close the connection to the database after running this notebook.

#### Build ETL Processes
- Follow instructions in the etl.ipynb notebook to develop ETL processes for each table. At the end of each table section, or at the end of the notebook, run test.ipynb to confirm that records were successfully inserted into each table. Remember to rerun create_tables.py to reset your tables before each time you run this notebook.

#### Build ETL Pipeline
- Use what you've completed in etl.ipynb to complete etl.py, where you'll process the entire datasets. Remember to run create_tables.py before running etl.py to reset your tables. Run test.ipynb to confirm your records were successfully inserted into each table.
