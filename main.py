from movie_app import MovieApp
from storage_csv import StorageCSV
from storage_json import StorageJson
import sys
import argparse


def is_valid_input(user_input, valid_input):
    return user_input in valid_input


def has_command_line_arg():
    """
    Checks if there are any command line arguments apart from the main.py arg.
    @return:
    """
    if len(sys.argv) > 1:
        return ".json" in sys.argv[1] or ".csv" in sys.argv[1]
    else:
        return False


def get_cla_filename():
    """
    Retrieves the filename and parses it to identify the file type so that the correct
    storage object can be instantiated in the main method.
    @return:
    """
    """
    file_path = sys.argv[1]
    file_type = file_path.split(".")[1]
    return file_path, file_type
    """
    parser = argparse.ArgumentParser(description="Parses the file type to initialize "
                                                 "the corresponding storage object")
    # parser.add_argument("file_path", metavar="file_path", type=str,
    #                    help="Enter python file + space + your_name + file_extension")
    parser.add_argument('file_path', metavar="file_path",
                        help="Enter python file + space + your_name + file_extension")
    args = parser.parse_args()
    if args.file_path:
        # return file_path and the extension type
        return args.file_path, args.file_path.split(".")[1]
    else:
        return None, None


def main():
    # Initialize local variables
    storage = None
    valid_files = ["csv", "json"]

    if has_command_line_arg():
        file_path, file_type = get_cla_filename()
        if file_path and file_type:
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
