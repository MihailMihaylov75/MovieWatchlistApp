__author__ = 'Mihail Mihaylov'
import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Add new user.
7) Search for a movie.
8) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()

user_input = input(menu)


def prompt_add_movie():
    """
    A function asking the user to add new movie and release date.
    :return:
    """
    title = input("Movie title: ")
    release_date = input('Release date in format dd-mm-YYYY: ')
    parsed_date = datetime.datetime.strptime(release_date, '%d-%m-%Y')
    timestamp = parsed_date.timestamp()
    database.add_movie(title, timestamp)


def print_movie_list(heading, movies):
    """
    A function that print all movies.
    :param heading: A message to be displayed
    :param movies: List of movies to print
    :return:
    """
    print('---{}---'.format(heading))
    for _id, title, release_timestamp in movies:
        movie_date = datetime.datetime.fromtimestamp(float(release_timestamp))
        human_date = movie_date.strftime('%b-%d-%Y')
        print('{} {} on {}.'.format(_id, title, human_date))


def prompt_watched_movie():
    """
    A function that allow a user to mark movie as watched.
    :return:
    """
    username = input('Enter a username: ')
    movie_id = input('Enter a movie ID: ')
    database.watch_movie(username, movie_id)


def prompt_add_user():
    """
    Add new user.
    :return:
    """
    username = input('Enter username: ')
    database.add_user(username)


def prompt_show_watched_movies():
    """
    Shows watched by user movies.
    :return:
    """
    username = input("Username: ")
    print(database.get_movies(username))
    movies = database.get_watched_movies(username)
    if movies:
        print_movie_list('Watched:', movies)
    else:
        print('The user has watched no movies yet.')


def prompt_search_movies():
    """
    Search for movies by given string.
    :return:
    """
    search_pattern = input('Enter movie title: ')
    movies = database.search_movies(search_pattern)
    if movies:
        print_movie_list('Movies found: ', movies)
    else:
        print('Found no movies for search pattern {}.'.format(search_pattern))


while user_input != "8":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list('Upcoming movies', movies)
    elif user_input == "3":
        movies = database.get_movies(False)
        print_movie_list('All movies', movies)
    elif user_input == "4":
        prompt_watched_movie()
    elif user_input == "5":
        prompt_show_watched_movies()
    elif user_input == '6':
        prompt_add_user()
    elif user_input == '7':
        prompt_search_movies()
    else:
        print("Invalid input, please try again!")
    user_input = input(menu)
