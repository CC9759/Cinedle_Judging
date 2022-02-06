"""
Functions for acquiring imdb information
author: Samson Zhang, Celina Chen, Jacob Swihart, Rahul Raiyani
"""
import imdb
import random

imdb_data = imdb.IMDb()


def get_top250():
    """
    returns the top 250 movies on imdb
    """
    return imdb_data.get_top250_movies()


def get_rand_movie():
    """
    gets a random movie from the top 250 movies
    """
    return get_top250()[random.randrange(250)]

def get_user_movie(user_input):
    """
    gets the users guess and returns the closest match
    """
    return imdb_data.search_movie(user_input)[0]['title']

def check_movie(user_input, answer):
    """
    checks if the user input matches the answer
    """
    movies = imdb_data.search_movie(user_input)
    return movies is not None and movies[0]['title'] == answer['title']
