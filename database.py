__author__ = 'Mihail Mihaylov'
import datetime
import sqlite3

CREATE_MOVIE_TABLE = """CREATE TABLE IF NOT EXISTS movies(
    title TEXT,
    release_timestamp TEXT,
    watched INTEGER
);"""
INSERT_INTO_MOVIES = """INSERT INTO movies(title, release_timestamp, watched)
    VALUES (?, ?, 0);"""
SELECT_ALL_MOVIES = """SELECT * FROM movies;"""
SELECT_UPCOMING_MOVIES = """SELECT * FROM movies WHERE release_timestamp > ?;"""
SELECT_WATCHED_MOVIES = "SELECT * FROM movies WHERE watched > 0;"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?"

connection = sqlite3.connect('data.db')
connection.row_factory = sqlite3.Row


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIE_TABLE)


def add_movies(title, release_timestamp):
    with connection:
        connection.execute(INSERT_INTO_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (timestamp, ))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor


def watch_movies(title):
    with connection:
        connection.execute(SET_MOVIE_WATCHED, (title,))


def get_watched_movies():
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES)
        return cursor
