Project 1: Data Modeling with Postgres
===============
Purpose of this database
---------------
This database offers a structured and easy way to query data fetched from 
song and song log dataset files. 

project dataset
---------------
This project process 101 files diveded into two types of files namely song and los files.
71 song files conating song data like: artist id, artist name, song id, song title, song duration, ... etc.
30 log files containging log data like: level, location, session Id, song, timestamp, user agent, user id, ... etc

How to run the Python scripts
---------------
In order to fetch and store the data from the dataset, three python scripts should be executed sql_queries, create_tables.py and etl.py . run the following commands in the console: 

1. python3 sql_queries
2. python3 create_tables.py
3. python3 etl.py

Files in the repository
---------------
1. Folder data contains a dataset of song and song log json files
2. sql_queries.py: contains create, read and drop table sql statements.
3. create_tables.py: contains functions to create and drop tables using sql statements from sql_queries file
4. elt.py: contains functions to process the dataset data with the help of sql statements from sql_queries filesql_queries
5. etl.ipynb: Juypter notebook to go step by step through the etl process
6. test.ipynb: Juypter notebook for tests


Database schema and ETL
---------------
As shown in the figure (please see database_schema.jpg, if the figure did not display inline), the tables are created as a stare schema where songplays is the fact table and the rest of the tables are dimension tables.
![The database schema!](https://github.com/BaZom/Data-warehouse-with-AWS-S3-and-Redshift/blob/848476c6f991f098374eba1e0247dcb8d3350468/star_schema.png?raw=true "")

ETL workflow: 
fetchting dataset files --> process and store song data --> process and store log data

Remarks on final results:
---------------

 - Duplications occuered in tables like songplays, users and time 
 - in songplays there can be duplications for the same user id in columns like: song_id, artist_id, session_id, Location and user_agent
 - in time table there be duplications for almost similar timestamps in columns like: hour 	day, week, month, year, weekday
 - users first and last names, also gender and level may be similar over multiple rows.
