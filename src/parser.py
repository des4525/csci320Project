import csv
import os
import re
import sys
from datetime import datetime
import random

import psycopg2

possible_genres = ['berlin minimal techno', 'japanese vtuber', 'meme rap', 'bubblegrunge', 'canadian contemporary r&b']


def randomize_listens():
    songs_query = '''
    SELECT "songid"
    FROM "Song";
    '''

    listens_thing = '''
    UPDATE "Song"
    SET "listens" = %s
    WHERE "songid" = %s;
    '''

    cursor = connection.cursor()
    cursor.execute(songs_query)
    songs = cursor.fetchall()

    for song in songs:
        listens = random.randint(100, 10000)
        try:
            cursor.execute(listens_thing, (listens, song[0]))
            print("Set song: {} listens to {}.".format(song[0], listens))
            connection.commit()
        except Exception as e:
            print e.message
            connection.rollback()

    cursor.close()


def get_release_date(song_id):
    date_query = '''
        SELECT "rdate" 
        FROM "Song"
        WHERE "songid" = %s;
    '''

    cursor = connection.cursor()
    cursor.execute(date_query, (song_id,))
    rdate = cursor.fetchall()
    cursor.close()
    print rdate
    return rdate


def get_artists():
    artist_query = '''
    SELECT "aname" FROM "Artist";
    '''

    cursor = connection.cursor()
    cursor.execute(artist_query)

    artists = cursor.fetchall()

    cursor.close()

    return artists


def create_albums(artist_name):
    song_query = '''
    SELECT "ArtistReleases"."songid"
    FROM ( "Artist" INNER JOIN "ArtistReleases" ON "Artist"."aname" = "ArtistReleases"."aname")
    WHERE "Artist"."aname" = %s;
    '''

    album_contain = '''
        INSERT INTO "AlbumContains"
        ("albumid", "songid", track_number)
        VALUES (%s, %s, %s);
    '''

    album_insertion = '''
        INSERT INTO "Album"
        ("albumid", "rdate", "name")
        VALUES (%s, %s, %s);
    '''

    cursor = connection.cursor()

    cursor.execute(song_query, (artist_name,))
    songs = cursor.fetchmany(10)
    album_number = 1
    album_name = "{} album {}".format(artist_name, album_number)
    album_id = songs[0][0]
    album_date = get_release_date(album_id)
    track = 1
    while songs:
        for song in songs:
            try:
                cursor.execute(album_insertion, (album_id, album_date[0], album_name,))
                cursor.execute(album_contain, (album_id, song[0], track))
                connection.commit()
                print "committed"
                track = track + 1
            except Exception as e:
                connection.rollback()
                print e.message
        album_number = album_number + 1
        track = 1
        try:
            songs = cursor.fetchmany(10)
            album_id = songs[0][0]
            album_name = "{} album {}".format(artist_name, album_number)
            album_date = get_release_date(album_id)
        except:
            break

    cursor.close()


def insert_song(row):
    attributes = []
    for a in row:
        attributes.append(a)

    song_name = attributes[12]
    song_id = attributes[6]
    artists = attributes[1]
    date_str = attributes[14]
    duration = int(attributes[3]) / 1000

    if "-" not in date_str:
        date_str = "{}-01-01".format(date_str)

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    song_insertion = '''
        INSERT INTO "Song"
        ("songid", "name", "rdate", "length")
        VALUES (%s, %s, %s, %s );
    '''

    cursor = connection.cursor()

    try:
        cursor.execute(song_insertion, (song_id, song_name, date_obj, duration))
        connection.commit()
    except:
        connection.rollback()

    if isinstance(artists, str):

        artists = artists[2:-2]

        artist_insertion = '''
                        INSERT INTO "Artist"
                        ("aname")
                        VALUES (%s);
                        '''

        try:
            cursor.execute(artist_insertion, (artists,))
            connection.commit()
        except:
            connection.rollback()

        artist_release = '''
                INSERT INTO "ArtistReleases"
                ("aname", "songid")
                VALUES (%s, %s);
                '''
        try:
            cursor.execute(artist_release, (artists, song_id,))
            connection.commit()
        except:
            connection.rollback()



    else:
        for artist in artists:
            artist = artist[2:-2]

            artist_insertion = '''
                    INSERT INTO "Artist"
                    ("name")
                    VALUES (%s);
                    '''

            try:
                cursor.execute(artist_insertion, artist)
                connection.commit()
            except:
                connection.rollback()

            artist_release = '''
            INSERT INTO "ArtistReleases"
            ("aname", "songid")
            VALUES (%s, %s);
            '''

            try:
                cursor.execute(artist_release, (artist, song_id))
                connection.commit()
            except:
                connection.rollback()

    song_genre = random.choice(possible_genres)
    print(song_genre)

    genre_classifies = '''
    INSERT INTO "GenreClassifies"
    ("gname", "songid")
    VALUES (%s, %s);
    '''

    try:
        cursor.execute(genre_classifies, (song_genre, song_id,))
        connection.commit()
    except:
        connection.rollback()

    cursor.close()


def main():
    data_ACOUSTICNESS = 0
    data_ARTISTS = 1
    data_DANCEABILITY = 2
    data_DURATION_MS = 3
    data_ENGERY = 4
    data_EXPLICIT = 5
    data_ID = 6
    data_INSTRUMENTALNESS = 7
    data_KEY = 8
    data_LIVENESS = 9
    data_LOUDNESS = 10
    data_MODE = 11
    data_NAME = 12
    data_POPULARITY = 13
    data_RELEASE_DATE = 14
    data_SPEECHINESS = 15
    data_TEMPO = 16
    data_VALNCE = 17
    data_YEAR = 18

    artist_ARTISTS = 0
    artist_ACOUSTICNESS = 1
    artist_DANCEABILITY = 2
    artist_DURATION_MS = 3
    artist_ENGERY = 4
    artist_INSTRUMENTALNESS = 5
    artist_KEY = 6
    artist_LIVENESS = 7
    artist_LOUDNESS = 8
    artist_POPULARITY = 9
    artist_SPEECHINESS = 10
    artist_TEMPO = 11
    artist_VALNCE = 12
    artist_YEAR = 13
    artist_COUNT = 14

    genre_GENRE = 0
    genre_ACOUSTICNESS = 1
    genre_DANCEABILITY = 2
    genre_DURATION_MS = 3
    genre_ENGERY = 4
    genre_INSTRUMENTALNESS = 5
    genre_LIVENESS = 6
    genre_LOUDNESS = 7
    genre_SPEECHINESS = 8
    genre_TEMPO = 9
    genre_VALNCE = 10
    genre_POPULARITY = 11
    genre_KEY = 12
    genre_MODE = 13

    year_YEAR = 0
    year_ACOUSTICNESS = 1
    year_DANCEABILITY = 2
    year_DURATION_MS = 3
    year_ENGERY = 4
    year_INSTRUMENTALNESS = 5
    year_LIVENESS = 6
    year_LOUDNESS = 7
    year_SPEECHINESS = 8
    year_TEMPO = 9
    year_VALNCE = 10
    year_POPULARITY = 11
    year_KEY = 12
    year_MODE = 13

    genreW_ARTISTS = 0
    genreW_ACOUSTICNESS = 1
    genreW_DANCEABILITY = 2
    genreW_DURATION_MS = 3
    genreW_ENGERY = 4
    genreW_INSTRUMENTALNESS = 5
    genreW_LIVENESS = 6
    genreW_LOUDNESS = 7
    genreW_SPEECHINESS = 8
    genreW_TEMPO = 9
    genreW_VALNCE = 10
    genreW_POPULARITY = 11
    genreW_KEY = 12
    genreW_MODE = 13
    genreW_COUNT = 14
    genreW_GENRE = 15

    usr = "p320_02c"
    pw = "40lmwVV8ftOn"

    global connection

    connection = psycopg2.connect("dbname=" + usr + " user=" + usr + " password=" + pw + " host=reddwarf.cs.rit.edu")

    print("Connected with: " + connection.dsn)

    dataCSV = open("Data/data.csv")
    artistCSV = open("Data/data_by_artist.csv")
    genreCSV = open("Data/data_by_genres.csv")
    yearCSV = open("Data/data_by_year.csv")
    genreWCSV = open("Data/data_w_genres.csv")

    data = {}
    # baseData = csv.reader(dataCSV)
    #
    # row = next(baseData)

    # for i in range(1000):
    #     row = next(baseData)
    #     insert_song(row)

    # artists = get_artists()
    # for artist in artists:
    #     print artist[0]
    #     create_albums(artist[0])

    randomize_listens()

    # for row in baseData:
    #     things = []
    #     for thing in row:
    #         things.append(thing)
    #     print(things)

    # for row in baseData:
    #     data[row[data_ID]] = [row]

    # artist = {}
    # baseArtist = csv.reader(artistCSV)
    # for row in baseArtist:
    #     artist[row[artist_ARTISTS]] = [row]
    #
    # genre = {}
    # baseGenre = csv.reader(genreCSV)
    # for row in baseGenre:
    #     genre[row[genre_GENRE]] = [row]
    #
    # year = {}
    # baseYear = csv.reader(yearCSV)
    # for row in baseYear:
    #     year[row[year_YEAR]] = [row]
    #
    # genreW = {}
    # genreWData = csv.reader(genreWCSV)
    # for row in genreWData:
    #     genreW[row[genreW_ARTISTS]] = [row]
    #
    # artistInsertQs = []
    # for k,v in artist.items():
    #     artistInsertQs.append("INSERT INTO artist name VALUES " + str(k))
    #
    # genreInsertQs = []
    # for k,v in genre.items():
    #     genreInsertQs.append("INSERT INTO genre name VALUES " + str(k))
    #
    # songInsertQd = []
    # for k,v in song.items():
    #     songInsertQs.append("INSERT INTO song name VALUES " + str(k))


if __name__ == "__main__":
    main()
