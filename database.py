__author__ = 'Mihail Mihaylov'

import os
import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s)"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
INSERT_USER = "INSERT INTO users (username) VALUES (%s)"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s)"
SELECT_WATCHED_MOVIES = """SELECT movies.*
    FROM users
    JOIN watched ON users.username = watched.user_username
    JOIN movies ON watched.movie_id = movies.id
    WHERE users.username = %s;"""
SEARCH_MOVIE = """SELECT * FROM movies WHERE title LIKE %s;"""

# Remember to not store the database URI in your code!
connection = psycopg2.connect(os.environ.get("DATABASE_URI"))


def create_tables():
    """
    Create the needed tables into database.
    :return:
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)


def add_movie(title, release_timestamp):
    """
    Add new movie into database.
    :param title: Title of the movie
    :param release_timestamp: Release date of the movie
    :return:
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (title, release_timestamp))


def get_movies(upcoming=False):
    """
    Get all movies from database.
    :param upcoming: Filter only  upcoming
    :return: Dictionary with all/upcoming movies
    """
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def add_user(username):
    """
    Add user to database.
    :param username:
    :return:
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def watch_movie(username, movie_id):
    """
    Marks a movie for a user as watched.
    :param username: The name of the user.
    :param movie_id: The ID of the movie
    :return:
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username):
    """
    Get watched movies by given user from database.
    :param username: The name of the user.
    :return: Dictionary with all watched movies by the user.
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()


def search_movies(search_term):
    """
    Search for movie by given pattern in database.
    :param search_term:
    :return: All movies that match the pattern
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIE, (f"%{search_term}%",))
            return cursor.fetchall()
