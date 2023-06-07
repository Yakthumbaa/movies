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
