import random
import math
import storage_json
import storage_csv

HTML_TEMPLATE = "index_template.html"
TITLE = "Masterschool's Movie App"
# Replace the "__ID_HERE__" placeholder with the movie's imdb id
IMDB_URL = "https://www.imdb.com/title/__ID_HERE__/"


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def get_storage(self):
        return self._storage

    @staticmethod
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

    def sort_movie_db(self, filename):
        """
        Method to sort the movies list of dictionaries - obtained from the current json file, by rating
        (descending order).
        # Code referenced from: https://shorturl.at/eszQ5 - not used but kept for further learning
        # sorted_list = sorted(movies_list, key=operator.itemgetter('rating'))
        :param filename:
        :return: sorted list of movies info dictionary
        """
        movies_list = self.get_storage().fetch_movie_data(filename)
        sorted_list = sorted(movies_list, key=lambda item: item['rating'], reverse=True)
        return sorted_list

    @staticmethod
    def get_average(movies_list):
        """
        Method to get the average rating. Called by get_stats() method.
        :param movies_list:
        :return:
        """
        num_of_movies = len(movies_list)
        ratings = [val for movies_dict in movies_list for key, val in movies_dict.items() if key == 'rating']
        """
        ^^^^ --> the one liner code above has replaced the block of code below
             --> left here for learning purpose...
        ratings = []
        for movies_dict in movies_list:
            for key, val in movies_dict.items():
                if key == "rating":
                    ratings.append(val)
        """
        sum_of_ratings = sum(ratings)
        average = round(sum_of_ratings / num_of_movies, 1)
        return average

    @staticmethod
    def get_median(movies_list):
        """
        Method to get the median rating. Called by get_stats() method.
        :param movies_list: This list is already sorted at the source
        :return:
        """
        num_of_movies = len(movies_list)
        if num_of_movies % 2 == 0:
            midpoint_1 = int(num_of_movies / 2) - 1
            value_mid_1 = movies_list[midpoint_1]["rating"]

            midpoint_2 = int(num_of_movies / 2 + 1) - 1
            value_mid_2 = movies_list[midpoint_2]["rating"]

            median = round((value_mid_1 + value_mid_2) / 2, 1)
        else:
            midpoint = int(math.ceil(num_of_movies / 2)) - 1
            median = movies_list[midpoint]["rating"]
        return median

    @staticmethod
    def get_best_worst(movies_list):
        """
        Method to get the best and the worst movies. Called by get_stats() method.
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

    def get_stats(self, filename):
        """
        Method to calculate the stats of the movies in the dictionary
        :param filename:
        :return:
        """
        # fetch the sorted list of movies dictionary
        sorted_movies_list = self.sort_movie_db(filename)
        # print(f"Movies_list = {sorted_movies_list}")  # @TEST
        num_of_movies = len(sorted_movies_list)
        # print(sorted_movies_list)  # -> @TEST
        print(f"\n{'*' * 10}\tStats\t{'*' * 10}")
        if num_of_movies:
            # Average rating
            print(f"Average rating: {self.get_average(sorted_movies_list)}")
            # Median rating
            print(f"Median rating: {self.get_median(sorted_movies_list)}")
            # Best and Worst
            best, worst = self.get_best_worst(sorted_movies_list)
            print("Best movie/s:")
            for movie in best:
                print(f"\t{movie['title']}")
            print("Worst movie/s:")
            for movie in worst:
                print(f"\t{movie['title']}")
        else:
            print("There is no movie in the list. Please add some...")
        print(f"{'*' * 10}\t END \t{'*' * 10}")

    def get_random(self, filename):
        """
        Method to get a random movie from the list
        :param filename:
        :return:
        """
        movies_list = self.get_storage().fetch_movie_data(filename)
        choices = [val for movie_dict in movies_list for key, val in movie_dict.items() if key == "title"]
        return random.choice(choices)

    def search_movie(self, filename):
        """
        Method to search for a movie in the file by title of the movie
        :param filename:
        :return:
        """
        display_properties = ["title", "rating", "country"]
        str_to_search = input("\nEnter part of movie name: ").title()
        movies_list = self.get_storage().fetch_movie_data(filename)
        counter = 0

        for movies_dict in movies_list:
            if str_to_search in movies_dict["title"]:
                counter += 1
                print(f"\n{'*' * 10}\tResults\t{'*' * 10}")
                for key, val in movies_dict.items():
                    if key in display_properties:
                        print(f"{key}: {val}")
                print(f"{'*' * 10}\t END \t{'*' * 10}")
        if counter == 0:
            print(f"'{str_to_search}' does not match any movie in the file...")
        """
        for movies_dict in movies_list:
            valid_condition = str_to_search in movies_dict["title"]
            print("\n".join(f"{key}: {val}" for key, val in movies_dict.items() if valid_condition
                  and not key == "poster_image_url"))
        for movies_dict in movies_list:
            print("\n".join(f"{key}: {val}" for key, val in movies_dict.items() if str_to_search in movies_dict["title"]
                            and not key == "poster_image_url"))
        """

    @staticmethod
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

    def get_html_txt(self, movies_list):
        """
        This method parses the movies list into a string in HTML language format by performing a method call on
        serialize_text(), which serializes the text input into the required HTML format.
        :param movies_list:
        :return:
        """
        text_for_html = ""
        for movie_info_dict in movies_list:
            text_for_html += self.serialize_text(movie_info_dict)
        return text_for_html

    def create_html_file(self, db_filename, html_filename):
        """
        This method parses the data from the movies list and replaces the placeholder in the html_template with
        the new content.
        :param db_filename:
        :param html_filename:
        :return: void
        """
        movies_list = self.get_storage().fetch_movie_data(db_filename)
        # print(movies_list)  # @TEST
        with open(HTML_TEMPLATE, "r") as reader:
            content = reader.read()
        # Prepare title
        content = content.replace("__TEMPLATE_TITLE__", TITLE)
        # Prepare movie lists  # @TEST
        html_text = self.get_html_txt(movies_list)
        content = content.replace("__TEMPLATE_MOVIE_GRID__", html_text)
        # print(content)  # @TEST
        with open(html_filename, "w") as writer:
            writer.write(content)
        print("Website generated successfully!")

    @staticmethod
    def display_home():
        """
        Home screen. A user can log in to their account to access their own
        movies database
        :return:
        """
        print("********** Movies App Login **********")
        print("\nMenu:")
        print("1. Login")
        print("2. Register")
        print("3. Forgot password")
        print("0. Exit")

    @staticmethod
    def display_menu(first_time=False):
        """
        This method displays all the options available to the user in the console
        :param first_time:
        :return:
        """
        # if this is the first time the program has run
        if first_time:
            print("********** My Movies Database **********")
        print("\nMenu:")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate website")
        print("0. Exit")

    def console(self, valid_choices, main_menu_prompt):
        """
        This method runs the program in a listener loop.
        :return:
        """
        # Initialize local variables
        storage = self.get_storage()
        filename = storage.get_file_path()
        # The data in this ^^^^^^^^^ file should be a list containing dictionaries with movie's information.
        # eg. [{key-value pairs of movie 1's info}, {key-value pairs of movie 2's info}]
        html_filename = "index.html"

        finished = False
        self.display_menu(first_time=True)

        while not finished:
            option = self.validate_input(main_menu_prompt, valid_choices)
            # Exit - DONE
            if option == 0:
                print("\n\t\t\t\t\t\t\tBye!!!")
                return
            # List movies - DONE
            elif option == 1:
                storage.list_movies(movies_list=None)
            # Add movie - DONE
            elif option == 2:
                storage.add_movie()
            # Delete movie - Done
            elif option == 3:
                storage.delete_movie()
            # Update Movie - Done
            elif option == 4:
                storage.update_movie()
            # Stats - Done
            elif option == 5:
                self.get_stats(filename)
            # Random movie - Done
            elif option == 6:
                random_movie = self.get_random(filename)
                print(f"\nRandom movie: {random_movie}")
            # Search movie - Done
            elif option == 7:
                self.search_movie(filename)
            # Sort movies by rating - Done
            elif option == 8:
                storage.list_movies(movies_list=self.sort_movie_db(filename))
            # Generate website
            elif option == 9:
                self.create_html_file(filename, html_filename)
            # Something went wrong. Continue with the program
            else:
                print("\nOops! Something went wrong! Please continue...\n")

            input("\nPress enter to continue")
            self.display_menu(first_time=False)

    def run_program(self):
        """
        This method wraps the program function in a try except to intercept a KeyboardInterrupt and prints
        a neat goodbye message instead of the exception!
        :return:
        """
        # Initialize the fields
        valid_choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        main_menu_prompt = f"\nEnter choice ({valid_choices[0]}-{valid_choices[-1]}): "
        try:
            self.console(valid_choices, main_menu_prompt)
        except KeyboardInterrupt:
            print("\n\t\t\t\t\t\t\tBye!!!")


def main():
    # Run the expression below once to load the country_code.json file with data formatted as:
    # {country_A: [code, flag_image_url], country_B: [code, flag_image_url]}
    # data_parser.load_countries_data()
    user_name = input("Enter your name: ")
    file_path_json = user_name + ".json"
    file_path_csv = user_name + ".csv"
    # storage = storage_json.StorageJson(file_path_json)
    storage = storage_csv.StorageCSV(file_path_csv)
    movie_app = MovieApp(storage)
    # print(storage)  # @TEST
    # print(type(storage))  # @TEST
    # print(storage.get_file_path())  # @TEST
    movie_app.run_program()


if __name__ == "__main__":
    main()
