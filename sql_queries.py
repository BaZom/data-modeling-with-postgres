# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

user_table_create = ("CREATE TABLE IF NOT EXISTS users (\
                        user_id INT primary key,\
                        first_name VARCHAR,\
                        last_name VARCHAR,\
                        gender VARCHAR,\
                        level VARCHAR);")

song_table_create = ("CREATE TABLE IF NOT EXISTS songs (\
                        song_id VARCHAR primary key,\
                        title VARCHAR not null,\
                        artist_id VARCHAR not null,\
                        year INT not null,\
                        duration numeric not null);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artists (artist_id VARCHAR primary key,\
                        name VARCHAR not null,\
                        location VARCHAR,\
                        latitude FLOAT,\
                        longitude FLOAT);")

time_table_create = ("CREATE TABLE IF NOT EXISTS time(\
                        start_time TIMESTAMP primary key,\
                        hour INT,\
                        day INT,\
                        week INT,\
                        month INT,\
                        year INT,\
                        weekday INT);")

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays (\
                            songplay_id serial primary key,\
                            start_time TIMESTAMP not null,\
                            user_id INT NOT NULL ,\
                            level VARCHAR,\
                            song_id VARCHAR,\
                            artist_id VARCHAR,\
                            session_id INT,\
                            location VARCHAR,\
                            user_agent TEXT,\
                            FOREIGN KEY(user_id) REFERENCES users(user_id),\
                            FOREIGN KEY(song_id) REFERENCES songs(song_id),\
                            FOREIGN KEY(artist_id) REFERENCES artists(artist_id),\
                            FOREIGN KEY(start_time) REFERENCES time(start_time));")
# INSERT RECORDS

songplay_table_insert = ("INSERT INTO songplays (start_time, user_id, level, song_id,\
                                                artist_id, session_id, location, user_agent)\
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)\
                                                ON CONFLICT DO NOTHING")

user_table_insert = ("INSERT INTO users (user_id, first_name, last_name, gender, level)\
                                 VALUES (%s, %s, %s, %s, %s)\
                                 ON CONFLICT(user_id) DO UPDATE \
                                 SET level = EXCLUDED.level")

song_table_insert = ("INSERT INTO songs (song_id, title, artist_id, year, duration)\
                                 VALUES (%s, %s, %s, %s, %s)\
                                 ON CONFLICT DO NOTHING")

artist_table_insert = ("INSERT INTO artists (artist_id,name, location, latitude, longitude)\
                                     VALUES (%s,%s, %s, %s, %s)\
                                     ON CONFLICT DO NOTHING")


time_table_insert = ("INSERT INTO time (start_time, hour, day, week, month, year, weekday)\
                                VALUES (%s, %s, %s, %s, %s, %s, %s)\
                                ON CONFLICT DO NOTHING")

# FIND SONGS
song_select = (" select s.song_id, a.artist_id\
                        from songs s join artists a\
                        on s.artist_id = a.artist_id\
                        where s.title = %s\
                        and a.name = %s\
                        and s.duration = %s")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]