import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """processes a song file from the dataset: 
           - reads data from file
           - prepare and store song data in songs table
           prepare and store artist data in arists table
    Args:
        curr (obj): object of curser class
        filepath (str): file path in the dataset
        
    Returns:
        no return values
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # prepare song data
    song_data_arr = df[['song_id','title','artist_id','year', 'duration']].values[0]    
    song_data = song_data_arr.tolist() 
    
    # insert song record
    cur.execute(song_table_insert, song_data)
    
    # prepare artist data
    artist_data_arr = df[['artist_id','artist_name', 'artist_location','artist_latitude', 'artist_longitude']].values[0]
    artist_data = artist_data_arr.tolist()
    
    # insert artist record
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """processes a log file from the dataset: 
           - reads data log file
           - prepare and store time data in time table
           - prepare abd store user data in user table
           - prepare and store data in songplay table
           
    Args:
        curr (obj): object of curser class
        filepath (str): file path in the dataset
        
    Returns:
        no return values
    """
        
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == "NextSong"]

    # convert timestamp column to datetime
    t = df['ts'].apply(pd.to_datetime)
    
    # prepare time data
    hour_list = t.dt.hour.tolist()
    day_list = t.dt.day.tolist()
    week_list = t.dt.week.tolist()
    month_list = t.dt.month.tolist()
    year_list = t.dt.week.tolist()
    weekend_list = t.dt.weekday.tolist()
    timestamp_list = t.tolist()
    
    time_data = list(zip(timestamp_list, hour_list, day_list, week_list, month_list, year_list, weekend_list))
    column_labels = ("timestamp", "hour", "day", "week", "month", "year", "weekday")
    
    # time dataframe
    time_df = pd.DataFrame(time_data, columns = column_labels)
    
    # insert time data records
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts), row.userId , row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """processes all files in the dataset: 
           - fetchs all files a given file path
           - processes data of fetched files with the help of the functions process_log_file and process_song_file
           
    Args:
        curr (obj): object of curser class
        conn (obj): database connection object
        filepath (str): folder path in the dataset
        func: log/data file process function
        
    Returns:
        no return values
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """establishes the connection to the database: 
           - fetchs all files a given file path
           - processes data of fetched files with the help of the functions:
                   -- process_log_file 
                   -- process_song_file
                       
    Args:
        no Args
        
    Returns:
        no return values
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()