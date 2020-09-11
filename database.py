__author__ = 'Mihail Mihaylov'
import datetime
import sqlite3

CREATE_MOVIE_TABLE = """CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
    );"""
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched(
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY (user_username) REFERENCES users(username),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);"""

INSERT_INTO_MOVIES = """INSERT INTO movies(title, release_timestamp)
    VALUES (?, ?);"""
INSERT_INTO_USERS = """INSERT INTO users(username) VALUES (?);"""
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = """SELECT * FROM movies;"""
SELECT_UPCOMING_MOVIES = """SELECT * FROM movies WHERE release_timestamp > ?;"""
SELECT_WATCHED_MOVIES = """SELECT movies.*
    FROM movies
    JOIN watched ON movies.id = watched.movie_id
    JOIN users ON users.username = watched.user_username
    WHERE users.username = ?;"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (?, ?);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"

connection = sqlite3.connect('data.db')
connection.row_factory = sqlite3.Row


def create_tables():
    with connection:
        connection.execute(CREATE_MOVIE_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)


def add_user(username):
    with connection:
        connection.execute(INSERT_INTO_USERS, (username,))


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


def watch_movie(username, movie_id):
    with connection:
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor
