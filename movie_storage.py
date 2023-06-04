import json
import requests
from abc import ABC, abstractmethod

API_KEY = "abc7bcb8"

# url format is API_URL_TITLE + "title"
API_URL_TITLE = f"http://www.omdbapi.com/?apikey={API_KEY}&t="

# url format is prefix + {"imdb id"} + suffix + API_KEY
API_URL_ID_PREFIX = f"http://www.omdbapi.com/?i="
API_URL_ID_SUFFIX = "&apikey="

# Default url vv
API_URL_DEFAULT = f"http://www.omdbapi.com/?apikey={API_KEY}&t=Titanic"

# Replace the ":country_code" placeholder with the country code
# style --> flat or shiny: size --> 64 is default
# Reference: https://flagsapi.com/#quick
FLAG_SIZE = "64"
FLAG_STYLE = "flat"
# The url to use in the Flag's API needs to be in the format:
# URL_FLAG_Prefix + country_code + FLAG_STYLE + FLAG_SIZE + URL_FLAG_SUFFIX
URL_FLAG_Prefix = "https://flagsapi.com/"
URL_FLAG_SUFFIX = ".png"


def fetch_movie_data(filename):
    """
    This method is to fetch the movies information data from the file with the filename that is
    passed as the argument.
    :param filename:
    :return:
    """
    with open(filename, "r") as reader:
        try:
            data = json.loads(reader.read())
        except json.decoder.JSONDecodeError:
            return []
        else:
            return data


def save_to_file(filename, new_content):
    """
    This method gets the new content as the argument, which is then parsed to overwrite the old content
    of the file in filename
    :param filename:
    :param new_content:
    :return:
    """
    content = json.dumps(new_content, indent=2)
    with open(filename, "w") as writer:
        writer.write(content)


def search_title_in_api(param, title=True, movie_id=False):
    """
    -->> Throws KeyError <<--
    -->> Throws ConnectionError <<--
    This method is used to make connection with the movie db API to perform search by title or
    id. This returns the dictionary with the movie's properties + values associated with the required keys
    from the dictionary returned by the response from the request to API.
    N.B. The search by title is only for future implementation. Not being used currently.
    :param param:
    :param title:
    :param movie_id:
    :return: movie info dictionary
    """
    # initialize url to fetch data
    if title:
        url = API_URL_TITLE + param
    elif movie_id:
        url = API_URL_ID_PREFIX + param + API_URL_ID_SUFFIX + API_KEY
    else:
        url = API_URL_DEFAULT  # Maybe this else is redundant

    # Catch ConnectionError Exception
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        movie_data_dict = {"Error": "ConnectionError"}
    else:
        movie_data_dict = response.json()

    # response.json() returns dictionary with keys "response" and "error" if unable to return movie's info
    # "response": False but "error" has a more descriptive value. Use "error" to handle exceptions.
    if not movie_data_dict["Response"]:
        if movie_data_dict["Error"] == "Movie not found!":
            raise KeyError  # This exception is handled by the caller in program_functions.py
        elif movie_data_dict["Error"] == "ConnectionError":
            raise ConnectionError  # This exception is handled by the caller in program_functions.py
    else:
        title = movie_data_dict["Title"]
        year = movie_data_dict["Year"]
        rating = movie_data_dict["imdbRating"]
        poster_image_url = movie_data_dict["Poster"]
        imdb_id = movie_data_dict["imdbID"]
        country = movie_data_dict["Country"].split(",")[0]
        flag_image_url = get_flag_url(country)
        return {"title": title, "year": int(year.split("–")[0]), "rating": float(rating),
                "poster_image_url": poster_image_url, "imdb_id": imdb_id, "country": country,
                "flag_image_url": flag_image_url}


def get_country_code(country):
    """
    This will get the country code associated to the name of the country passed as the argument
    :param country:
    :return:
    """
    file_to_read = "../movies/country_code.json"
    with open(file_to_read, "r") as reader:
        country_data = json.loads(reader.read())
    return country_data[country][0]


def get_flag_url(country):
    """
    This will get the flag url associated to the name of the country passed as the argument
    :param country:
    :return:
    """
    file_to_read = "../movies/country_code.json"
    with open(file_to_read, "r") as reader:
        country_data = json.loads(reader.read())
    return country_data[country][1]


def load_countries_data():
    """
    This method loads the country_code.csv file downloaded online into a country_code.json file. The data structure
    will be a nested dictionary with country's name as key and a list of code and flag url str as its values.
    The data is also available at https://flagcdn.com/en/codes.json
    Using a downloaded data for good measure.
    :return: void
    """
    file_to_read = "../movies/country_code.csv"
    file_to_write = "../movies/country_code.json"
    with open(file_to_read, "r") as reader:
        data = reader.readlines()[1:-1]
    country_data = {}
    for line in data:
        if not line.split(",")[0] == "Name" and not line.split(",")[1] == "Code" and line:
            country = line.split(",")[0]  # .replace('"', "")
            code = line.split(",")[-1][:-1]  # .replace('"', "")
        """
        The expression below only replaced the last ":size" str with flag_size. The rest of the str stayed the same.
        for place_holder in ((":country_code", f"{code}"), (":style", f"{FLAG_STYLE}"), (":size", f"{FLAG_SIZE}")):
            flag = API_URL_FLAG.replace(*place_holder)
        """
        flag_image_url = URL_FLAG_Prefix + code + "/" + FLAG_STYLE + "/" + FLAG_SIZE + URL_FLAG_SUFFIX
        country_data[country] = [code, flag_image_url]
    save_to_file(file_to_write, country_data)
