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
7) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()

user_input = input(menu)


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input('Release date in format dd-mm-YYYY: ')
    parsed_date = datetime.datetime.strptime(release_date, '%d-%m-%Y')
    timestamp = parsed_date.timestamp()
    database.add_movies(title, timestamp)


def print_movie_list(heading, movies):
    print('---{}---'.format(heading))
    for _id, title, release_timestamp in movies:
        movie_date = datetime.datetime.fromtimestamp(float(release_timestamp))
        human_date = movie_date.strftime('%b-%d-%Y')
        print('ID:{} of movie {} on {}.'.format(_id, title, human_date))


def prompt_watched_movie():
    username = input('Enter a username: ')
    movie_id = input('Enter a movie ID: ')
    database.watch_movie(username, movie_id)


def prompt_add_user():
    username = input('Enter username: ')
    database.add_user(username)


def prompt_show_watched_movies():
    username = input("Username: ")
    movies = database.get_watched_movies(username)
    if movies:
        print_movie_list('Watched:', movies)
    else:
        print('The user has watched no movies yet.')


while user_input != "7":
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
    else:
        print("Invalid input, please try again!")
    user_input = input(menu)
