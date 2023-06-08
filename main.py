from movie_app import MovieApp
from storage_csv import StorageCSV
from storage_json import StorageJson
import sys


def is_valid_input(user_input, valid_input):
    return user_input in valid_input


def has_command_line_arg():
    """

    @return:
    """
    for arg in sys.argv:
        print(arg)
    condition_1 = sys.argv[0] == "main.py"
    condition_2 = ".json" in sys.argv[1] or ".csv" in sys.argv[1]
    return condition_1 and condition_2


def get_cla_filename():
    file_path = sys.argv[1]
    if file_path.split(".")[1] == "csv":
        file_type = "csv"
    else:
        file_type = "json"
    return file_path, file_type


def main():
    # Initialize local variables
    storage = None
    valid_files = ["csv", "json"]

    if has_command_line_arg():
        file_path, file_type = get_cla_filename()
        if file_type == "csv":
            storage = StorageCSV(file_path)
        else:
            storage = StorageJson(file_path)
    else:
        try:
            while True:
                file_option = input("choose file type (csv) or (json): ").lower()
                if is_valid_input(file_option, valid_files):
                    user_name = input("Enter your name: ").lower()
                    break
                else:
                    print("Please type 'csv' or 'json'...")
        except KeyboardInterrupt:
            print("\n\n\t\t********  Goodbye!  ********")
        else:
            if file_option == "csv":
                file_path = user_name + ".csv"
                storage = StorageCSV(file_path)
            else:
                file_path = user_name + ".json"
                storage = StorageJson(file_path)

    movie_app = MovieApp(storage)
    movie_app.run_program()


if __name__ == "__main__":
    main()