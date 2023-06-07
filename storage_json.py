from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        super().__init__(file_path)

    def fetch_movie_data(self, filename):
        """
        This method is to fetch the movies information data from the file with the filename that is
        passed as the argument.
        :param filename:
        :return:
        """
        while True:
            try:
                with open(filename, "r") as reader:
                    try:
                        data = json.loads(reader.read())
                    except json.decoder.JSONDecodeError:
                        return []
                    else:
                        return data
            except FileNotFoundError:
                self.save_to_file(filename)
                """
                with open(filename, "r") as reader:
                    try:
                        data = json.loads(reader.read())
                    except json.decoder.JSONDecodeError:
                        return []
                    else:
                        return data
                """
                return []

    def save_to_file(self, filename, new_content=None):
        """
        This method gets the new content as the argument, which is then parsed to overwrite the old content
        of the file in filename
        :param filename:
        :param new_content:
        :return:
        """
        if new_content is not None:
            content = json.dumps(new_content, indent=2)
        else:
            content = json.dumps([], indent=2)
        with open(filename, "w") as writer:
            writer.write(content)

    def list_movies(self, movies_list=None):
        """
        Method to list all the movies + ratings from the movies dictionary
        :param movies_list:
        :return:
        """
        # dict_to_return = {}
        if movies_list is None:
            movies_list = self.fetch_movie_data(self.file_path)
        num_movies = len(movies_list)
        # print(f"num_movies: {num_movies}")  # -> @TEST
        print(f"\n{num_movies} movies in total")
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
            print(f"{title.title()} has been successfully deleted!\n")
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
