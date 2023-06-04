import math
import random
import movie_storage
import movies

HTML_TEMPLATE = "index_template.html"
TITLE = movies.TITLE
# Replace the "__ID_HERE__" placeholder with the movie's imdb id
IMDB_URL = "https://www.imdb.com/title/__ID_HERE__/"


def sort_movie_db(filename):
    """
    Method to sort the movies list of dictionaries - obtained from the current json file, by rating
    (descending order).
    # Code referenced from: https://shorturl.at/eszQ5 - not used but kept for further learning
    # sorted_list = sorted(movies_list, key=operator.itemgetter('rating'))
    :param filename:
    :return: sorted list of movies info dictionary
    """
    movies_list = movie_storage.fetch_movie_data(filename)
    sorted_list = sorted(movies_list, key=lambda item: item['rating'], reverse=True)
    return sorted_list


'''
This method is not being used currently. Obsolete but not deleted!
def sort_movie_list(movies_list):
    """
    Method to sort the movies list of dictionaries - list is passed as argument, by rating(descending order).
    :param movies_list:
    :return: sorted list of movies info dictionary
    """
    sorted_list = sorted(movies_list, key=lambda item: item['rating'], reverse=True)
    return sorted_list
'''


def list_movies(filename, movies_list=None):
    """
    Method to list all the movies + ratings from the movies dictionary
    :param movies_list:
    :param filename:
    :return:
    """
    if movies_list is None:
        movies_list = movie_storage.fetch_movie_data(filename)
    num_movies = len(movies_list)
    print(f"\n{num_movies} movies in total")
    if num_movies:
        for movies_info_dict in movies_list:
            print(f"{movies_info_dict['title']}: {movies_info_dict['rating']}")
    else:
        print("\nPlease add a movie!")


def add_movie(filename):
    """
    Method to add a movie
    :param filename:
    :return:
    """
    movies_list = movie_storage.fetch_movie_data(filename)
    title = input("\nEnter new movie name: ").title()
    try:
        movies_data = movie_storage.search_title_in_api(title, title=True, movie_id=False)
    except KeyError:
        print(f"\nThere is no movie called '{title}' in the Database!")
        return
    except ConnectionError:
        print("\nCould not connect to the internet. Please check your connection...")
        return
    else:
        # validate entry - To ensure no duplicate entries!
        list_of_movies = [title for movies_dict in movies_list for key, title in movies_dict.items() if key == "title"]
        if movies_data["title"] not in list_of_movies:
            movies_list.append(movies_data)
            movie_storage.save_to_file(filename, movies_list)
            print(f"\nMovie '{movies_data['title']}' successfully added!")
        else:
            print(f"\nMovie '{movies_data['title']}' is already in the file!")
    # print(movies_list)  # @TEST


def delete_movie(filename):
    """
    Method to delete a movie from the json file
    :param filename:
    :return:
    """
    title = input("\nEnter movie name to delete: ").title()
    current_movies_data = movie_storage.fetch_movie_data(filename)
    try:
        # movie_storage.del_movie(filename, title)
        new_movies_data = [i for i in current_movies_data if not (i['title'] == title)]
    except KeyError:
        print("No such movie exists")
    else:
        movie_storage.save_to_file(filename, new_movies_data)
        print(f"{title} has been successfully deleted!\n")


def update_movies(filename):
    """
    Method to update the rating of a movie in the list
    :param filename:
    :return:
    """
    movies_list = movie_storage.fetch_movie_data(filename)
    title = input("\nEnter movie name: ").title()
    values = [val for dic in movies_list for val in dic.values()]

    if title in values:
        movie_note = input("Enter movie notes: ")
        for movie in movies_list:
            if movie['title'] == title:
                movie['movie_note'] = movie_note
        movie_storage.save_to_file(filename, movies_list)
        print(f"{title}: {movie_note} || Successfully updated!")
    else:
        print("\nMovie not in the list!")


def get_average(movies_list):
    """
    Low level method to get the average rating. Called by get_stats() method.
    :param movies_list:
    :return:
    """
    num_of_movies = len(movies_list)
    ratings = [val for movies_dict in movies_list for key, val in movies_dict.items() if key == 'rating']
    """
    ^^^^ --> the one liner code above has replaced the block of code below
    ratings = []
    for movies_dict in movies_list:
        for key, val in movies_dict.items():
            if key == "rating":
                ratings.append(val)
    """
    sum_of_ratings = sum(ratings)
    average = round(sum_of_ratings / num_of_movies, 1)
    return average


def get_median(movies_list):
    """
    Low level method to get the median rating. Called by get_stats() method.
    :param movies_list: This list is already sorted at the source
    :return:
    """
    num_of_movies = len(movies_list)
    if num_of_movies % 2 == 0:
        midpoint_1 = int(num_of_movies / 2)
        value_mid_1 = movies_list[midpoint_1]["rating"]

        midpoint_2 = int(num_of_movies / 2 + 1)
        value_mid_2 = movies_list[midpoint_2]["rating"]

        median = round((value_mid_1 + value_mid_2) / 2, 1)
    else:
        midpoint = int(math.ceil(num_of_movies / 2))
        median = movies_list[midpoint]["rating"]
    return median


def get_best_worst(movies_list):
    """
    Low level method to get the best and the worst movies. Called by get_stats() method.
    # Code referenced from: https://www.geeksforgeeks.org/python-find-dictionary-matching-value-in-list/
    # best_movies = next((movies_dict for movies_dict in movies_list if movies_dict['rating'] == max_val),
    :param movies_list:
    :return:
    """
    ratings = [val for movies_dict in movies_list for key, val in movies_dict.items() if key == "rating"]
    max_val = max(ratings)
    min_val = min(ratings)
    best_movies = [movies_dict for movies_dict in movies_list if movies_dict["rating"] == max_val]
    worst_movies = [movies_dict for movies_dict in movies_list if movies_dict["rating"] == min_val]
    return best_movies, worst_movies


def get_stats(filename):
    """
    Method to calculate the stats of the movies in the dictionary
    :param filename:
    :return:
    """
    # fetch the sorted list of movies dictionary
    movies_list = sort_movie_db(filename)
    print(f"\n{'*' * 10}\tStats\t{'*' * 10}")
    # Average rating
    print(f"\nAverage rating: {get_average(movies_list)}")
    # Median rating
    print(f"Median rating: {get_median(movies_list)}")
    # Best and Worst
    best, worst = get_best_worst(movies_list)
    print("\nBest movie/s:")
    for movie in best:
        print(movie["title"])
    print("\nWorst movie/s:")
    for movie in worst:
        print(movie["title"])
    print(f"\n{'*' * 10}\t END \t{'*' * 10}")


def get_random(filename):
    """
    Method to get a random movie from the list
    :param filename:
    :return:
    """
    movies_list = movie_storage.fetch_movie_data(filename)
    choices = [val for movie_dict in movies_list for key, val in movie_dict.items() if key == "title"]
    return random.choice(choices)


def search_movie(filename):
    """
    Method to search for a movie in the movies_data.json file by title of the movie
    :param filename:
    :return:
    """
    str_to_search = input("\nEnter part of movie name: ").lower().title()
    movies_list = movie_storage.fetch_movie_data(filename)

    for movies_dict in movies_list:
        if str_to_search in movies_dict["title"]:
            print()
            for key, val in movies_dict.items():
                if not key == "poster_image_url":
                    print(f"{key}: {val}")
    """
    for movies_dict in movies_list:
        valid_condition = str_to_search in movies_dict["title"]
        print("\n".join(f"{key}: {val}" for key, val in movies_dict.items() if valid_condition
              and not key == "poster_image_url"))
    for movies_dict in movies_list:
        print("\n".join(f"{key}: {val}" for key, val in movies_dict.items() if str_to_search in movies_dict["title"]
                        and not key == "poster_image_url"))
    """


def serialize_text(movies_info_dict):
    """
    This method is used to serialize the data in the movies_list to a html string format. This formatted string will
    go in place of a pre-determined str placeholder in the template.html file.
    >> Refer to "demo.html" file for reference <<
    :param movies_info_dict:
    :return:
    """
    imdb_link = IMDB_URL.replace("__ID_HERE__", movies_info_dict["imdb_id"])
    text_for_html = ('\n\t\t<li>' +
                     '\n\t\t\t<div class="movie">' +
                     f'\n\t\t\t\t<a href="{imdb_link}" target="_blank">' +
                     '\n\t\t\t\t\t<img class="movie-poster"' +
                     f'\n\t\t\t\t\t\tsrc="{movies_info_dict["poster_image_url"]}"')
    try:
        # Source: https://stackoverflow.com/questions/14263594/how-to-show-text-on-image-when-hovering
        text_for_html += f'\n\t\t\t\t\t\ttitle="{movies_info_dict["movie_note"]}"/>'
    except KeyError:
        text_for_html += f'\n\t\t\t\t\t\ttitle=""/>'
    text_for_html += ('\n\t\t\t\t</a>' +
                      f'\n\t\t\t\t<div class="movie-title">{movies_info_dict["title"]}</div>' +
                      f'\n\t\t\t\t<div class="movie-year">{movies_info_dict["year"]}</div>' +
                      f'\n\t\t\t\t<div class="movie-rating">IMDB: {movies_info_dict["rating"]}</div>' +
                      '\n\t\t\t\t<img class="movie-flag"' +
                      f'\n\t\t\t\t\tsrc="{movies_info_dict["flag_image_url"]}"' +
                      f'\n\t\t\t\t\ttitle=""/>'
                      '\n\t\t\t</div>' +
                      '\n\t\t</li>\n')
    return text_for_html


def get_html_txt(movies_list):
    """
    This method parses the movies list into a string in HTML language format by performing a method call on
    serialize_text(), which serializes the text input into the required HTML format.
    :param movies_list:
    :return:
    """
    text_for_html = ""
    for movie_info_dict in movies_list:
        text_for_html += serialize_text(movie_info_dict)
    return text_for_html


def create_html_file(db_filename, html_filename):
    """
    This method parses the data from the movies list and replaces the placeholder in the html_template with
    the new content.
    :param db_filename:
    :param html_filename:
    :return: void
    """
    movies_list = movie_storage.fetch_movie_data(db_filename)
    # print(movies_list)
    with open(HTML_TEMPLATE, "r") as reader:
        content = reader.read()
    # Prepare title
    content = content.replace("__TEMPLATE_TITLE__", TITLE)
    # Prepare movie lists  # @TEST
    html_text = get_html_txt(movies_list)
    content = content.replace("__TEMPLATE_MOVIE_GRID__", html_text)
    # print(content)  # @TEST
    with open(html_filename, "w") as writer:
        writer.write(content)
    print("Website generated successfully!")


def validate_input(prompt, valid_choices):
    """
    Method to validate the user input. The option input has to be an int
    :param prompt:
    :param valid_choices:
    :return:
    """
    valid = False
    while not valid:
        user_input = input(prompt)
        try:
            option = int(user_input)
        except ValueError:
            print("\nInvalid command! Please enter an integer...")
        else:
            if option in valid_choices:
                return option
            else:
                print("\nInvalid option!")
