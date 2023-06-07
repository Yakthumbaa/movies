from abc import ABC, abstractmethod
import requests
import json

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


class IStorage(ABC):
    """

    """

    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def fetch_movie_data(self, filename):
        pass

    @abstractmethod
    def save_to_file(self, filename, new_content=None):
        pass

    def list_movies(self, movies_list=None):
        """
        Method to list all the movies + ratings from the movies dictionary
        :param movies_list:
        :return:
        """
        if movies_list is None:
            movies_list = self.fetch_movie_data(self.file_path)
        num_movies = len(movies_list)
        # print(f"num_movies: {num_movies}")  # -> @TEST
        # print(f"\n{num_movies} movies in total")  # -> @TEST
        if num_movies:
            for movies_info_dict in movies_list:
                print(f"{movies_info_dict['title']}: {movies_info_dict['rating']}")
        else:
            print("Please add a movie!")

    def add_movie(self):
        """
        Method to add a movie
        :return:
        """
        movies_list = self.fetch_movie_data(self.file_path)
        # print(f"Movies_list: {movies_list}")  # -> @TEST
        title = input("\nEnter new movie name: ").title()
        try:
            movies_data = self.search_title_in_api(title, title=True, movie_id=False)
            # print(f"Movies_data: {movies_data}")  # -> @TEST
        except KeyError:
            print(f"\nThere is no movie called '{title}' in the Database!")
            return
        except ConnectionError:
            print("\nCould not connect to the internet. Please check your connection...")
            return
        else:
            # validate entry - To ensure no duplicate entries!
            list_of_movies = [title for movies_dict in movies_list for key, title in movies_dict.items() if
                              key == "title"]
            if movies_data["title"] not in list_of_movies:
                movies_list.append(movies_data)
                self.save_to_file(self.file_path, movies_list)
                print(f"\nMovie '{movies_data['title']}' successfully added!")
            else:
                print(f"\nMovie '{movies_data['title']}' is already in the file!")
        # print(movies_list)  # @TEST

    def delete_movie(self):
        """
        Method to delete a movie from the json file
        :return:
        """
        title = input("\nEnter movie name to delete: ").lower()
        current_movies_data = self.fetch_movie_data(self.file_path)
        # print(f"Current movies data: {current_movies_data}")  # -> @TEST
        movie_titles_in_file = [title.lower() for movies_dict in current_movies_data
                                for key, title in movies_dict.items() if key == "title"]
        # print(f"Movie titles: {movie_titles_in_file}")  # -> @TEST
        if title in movie_titles_in_file:
            new_movies_data = [i for i in current_movies_data if not (i['title'].lower() == title)]
            # print(f"New list: {new_movies_data}")  # -> @TEST
            self.save_to_file(self.file_path, new_movies_data)
            print(f"Movie '{title.title()}' has been successfully deleted!\n")
        else:
            print(f"'{title.title()}' movie does not exist")
        """
        try:
            # movie_storage.del_movie(filename, title)
            # new_movies_data = [i for i in current_movies_data if not (i['title'] == title)]
        except KeyError:
            print("No such movie exists")
        else:
            data_parser.save_to_file(self.file_path, new_movies_data)
            print(f"{title} has been successfully deleted!\n")
        """

    def update_movie(self):
        """
        Method to update the rating of a movie in the list
        :return:
        """
        movies_list = self.fetch_movie_data(self.file_path)
        title = input("\nEnter movie name: ").title()
        values = [val for dic in movies_list for val in dic.values()]

        if title in values:
            movie_note = input("Enter movie notes: ")
            for movie in movies_list:
                if movie['title'] == title:
                    movie['movie_note'] = movie_note
            self.save_to_file(self.file_path, movies_list)
            print(f"{title}: {movie_note} || Successfully updated!")
        else:
            print("\nMovie not in the list!")

    # ----------------------------------------- FLAG ----------------------------------------- #
    # ---------------------------------------------------------------------------------------- #

    @staticmethod
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

    def load_countries_data(self):
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
            data = [line for line in reader.readlines() if line]
        country_data = {}
        for line in data:
            if not line.split(",")[0] == "Name" and not line.split(",")[1] == "Code" and line:
                country = line.split(",")[0]  # .replace('"', "")
                code = line.split(",")[-1][:-1]  # .replace('"', "")
            else:
                continue
            flag_image_url = URL_FLAG_Prefix + code + "/" + FLAG_STYLE + "/" + FLAG_SIZE + URL_FLAG_SUFFIX
            country_data[country] = [code, flag_image_url]
        self.save_to_file(file_to_write, country_data)

    @staticmethod
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

    # ---------------------------------------------------------------------------------------- #
    # ----------------------------------------- FLAG ----------------------------------------- #

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, new_file_path):
        self.file_path = new_file_path

    def search_title_in_api(self, param, title=True, movie_id=False):
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
        # Initialize the required keys and the dictionary to return
        required_keys = {"title": "Title", "year": "Year", "rating": "imdbRating",
                         "poster_image_url": "Poster", "imdb_id": "imdbID", "country": "Country"}
        dict_to_return = {}

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
            for key, val in required_keys.items():
                try:
                    if key == "year":
                        dict_to_return[key] = int(movie_data_dict[val].split(",")[0])
                    elif key == "rating":
                        dict_to_return[key] = float(movie_data_dict[val].split(",")[0])
                    else:
                        dict_to_return[key] = movie_data_dict[val].split(",")[0]
                except KeyError:
                    if key == "rating":
                        dict_to_return[key] = 0
                    else:
                        continue
                except ValueError:
                    if key == "rating":
                        dict_to_return[key] = 0
                    else:
                        continue
            flag_image_url = self.get_flag_url(movie_data_dict["Country"].split(",")[0])
            dict_to_return["flag_image_url"] = flag_image_url
            return dict_to_return
