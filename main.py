from movie_app import MovieApp
from storage_csv import StorageCSV
from storage_json import StorageJson


def is_valid_input(user_input, valid_input):
    return user_input in valid_input


def main():
    valid_files = ["csv", "json"]
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