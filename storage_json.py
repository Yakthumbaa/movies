from istorage import IStorage
import data_parser


class StorageJson(IStorage):
    def __init__(self, file_path):
        super().__init__(file_path)

    def list_movies(self, movies_list=None):
        """
        Method to list all the movies + ratings from the movies dictionary
        :param movies_list:
        :return:
        """
        # dict_to_return = {}
        if movies_list is None:
            movies_list = data_parser.fetch_movie_data(self.file_path)
        num_movies = len(movies_list)
        print(f"num_movies: {num_movies}")
        print(f"\n{num_movies} movies in total")
        if num_movies:
            for movies_info_dict in movies_list:
                print(f"{movies_info_dict['title']}: {movies_info_dict['rating']}")
        else:
            print("\nPlease add a movie!")

    def add_movie(self):
        """
        Method to add a movie
        :return:
        """
        movies_list = data_parser.fetch_movie_data(self.file_path)
        print(f"Movies_list: {movies_list}")  # -> @TEST
        title = input("\nEnter new movie name: ").title()
        try:
            movies_data = data_parser.search_title_in_api(title, title=True, movie_id=False)
            print(f"Movies_data: {movies_data}")  # -> @TEST
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
                data_parser.save_to_file(self.file_path, movies_list)
                print(f"\nMovie '{movies_data['title']}' successfully added!")
            else:
                print(f"\nMovie '{movies_data['title']}' is already in the file!")
        # print(movies_list)  # @TEST

    def delete_movie(self):
        """
        Method to delete a movie from the json file
        :return:
        """
        title = input("\nEnter movie name to delete: ").title()
        current_movies_data = data_parser.fetch_movie_data(self.file_path)
        try:
            # movie_storage.del_movie(filename, title)
            new_movies_data = [i for i in current_movies_data if not (i['title'] == title)]
        except KeyError:
            print("No such movie exists")
        else:
            data_parser.save_to_file(self.file_path, new_movies_data)
            print(f"{title} has been successfully deleted!\n")

    def update_movie(self):
        """
        Method to update the rating of a movie in the list
        :return:
        """
        movies_list = data_parser.fetch_movie_data(self.file_path)
        title = input("\nEnter movie name: ").title()
        values = [val for dic in movies_list for val in dic.values()]

        if title in values:
            movie_note = input("Enter movie notes: ")
            for movie in movies_list:
                if movie['title'] == title:
                    movie['movie_note'] = movie_note
            data_parser.save_to_file(self.file_path, movies_list)
            print(f"{title}: {movie_note} || Successfully updated!")
        else:
            print("\nMovie not in the list!")
