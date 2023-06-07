import csv
from istorage import IStorage
import json
import storage_json


class StorageCSV(IStorage):

    def __init__(self, file_path):
        super().__init__(file_path)

    def fetch_movie_data(self, filename):
        """
        This method is to fetch the movies information data from the file with the filename that is
        passed as the argument.
        --> Reference:
        https://stackoverflow.com/questions/33547790/how-to-convert-string-values-to-integer-values-while-reading-a-csv-file
        https://stackoverflow.com/questions/21572175/convert-csv-file-to-list-of-dictionaries
        :param filename:
        :return:
        """
        while True:
            try:
                with open(filename, "r", newline='') as csv_file:
                    csv_reader = csv.DictReader(csv_file, skipinitialspace=True)
                    data = []
                    for row in csv_reader:
                        movie_dict = {}
                        for key, val in row.items():
                            if key == "year":
                                movie_dict[key] = int(val)
                            elif key == "rating":
                                movie_dict[key] = float(val)
                            else:
                                movie_dict[key] = val
                        data.append(movie_dict)
                    """
                    data = [{key: val for key, val in row.items() }
                            for row in csv_reader]
                    """
                    # print(f"Fetch movie method fetched: {data}")  # @TEST
                    return data
            except FileNotFoundError:
                self.save_to_file(filename)
                return []

    def save_to_file(self, filename, movies_list=None):
        """
        Saves the movie info list to the filename in a csv format.
        of the file in filename.
        --> reference:
        https://stackoverflow.com/questions/58513909/python-write-dictionary-to-csv-with-header
        :param filename: The filepath that the new csv file will be saved as
        :param movies_list: This is a list of dictionary/ies
        :return: None
        """
        with open(filename, "w", newline='') as csv_file:
            if movies_list is None:  # Simply create an empty csv file and return
                return
            else:
                fieldnames = [key for key, val in movies_list[0].items()]  # Initialize the datum header values
                # print(fieldnames)  # @TEST
                additional_header = [key for movie_data_dict in movies_list
                                     for key, val in movie_data_dict.items()
                                     if key not in fieldnames]
                fieldnames.extend(additional_header)
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()  # write the header
                for movie_data_dict in movies_list:
                    # row = [val for key, val in movie_data_dict.items()]  # @TEST
                    # print(f"Row: {row}")  # @TEST
                    writer.writerow(movie_data_dict)
