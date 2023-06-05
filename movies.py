"""
This code is divided into multiple files according to their roles.
--> movies.py: This is the MAIN file to run the movies program. This is the file that contains all the
    functionality of a console. The code is run in a listener loop calls different functions from the
    program_function file depending on the user's input.
--> program_functions.py: This file contains all the high level methods that is called by the console.
    It also contains some low level methods that takes the movies_list as a parameter. High level methods
    take the json filename as the parameter to get the updated movies list.
--> data_parser.py: This file has the methods to parse data and handles all the data parsing requirements
"""
import program_functions
import data_parser
import storage_json

TITLE = "Masterschool's Movie App"


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


def console(storage):
    """
    This method runs the program in a listener loop.
    :param storage: storage object (json or csv)
    :return:
    """
    # Initialize the fields
    valid_choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    filename = storage.get_file_path()
    html_filename = "index.html"
    # The data in this ^^^^^^^^^ file should be a list containing dictionaries with movie's information.
    # eg. [{key-value pairs of movie 1's info}, {key-value pairs of movie 2's info}]
    main_menu_prompt = f"\nEnter choice ({valid_choices[0]}-{valid_choices[-1]}): "
    finished = False
    display_menu(first_time=True)

    while not finished:
        option = program_functions.validate_input(main_menu_prompt, valid_choices)
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
            program_functions.get_stats(filename)
        # Random movie - Done
        elif option == 6:
            random_movie = program_functions.get_random(filename)
            print(f"\nRandom movie: {random_movie}")
        # Search movie - Done
        elif option == 7:
            program_functions.search_movie(filename)
        # Sort movies by rating - Done
        elif option == 8:
            storage.list_movies(movies_list=program_functions.sort_movie_db(filename))
        # Generate website
        elif option == 9:
            program_functions.create_html_file(filename, html_filename)
        # Something went wrong. Continue with the program
        else:
            print("\nOops! Something went wrong! Please continue...\n")

        input("\nPress enter to continue")
        display_menu(first_time=False)


def run_program(storage):
    """
    This method wraps the program function in a try except to intercept a KeyboardInterrupt and prints
    a neat goodbye message instead of the exception!
    :param storage:
    :return:
    """
    try:
        console(storage)
    except KeyboardInterrupt:
        print("\n\t\t\t\t\t\t\tBye!!!")


def main():
    # Run the expression below once to load the country_code.json file with data formatted as:
    # {country_A: [code, flag_image_url], country_B: [code, flag_image_url]}
    # data_parser.load_countries_data()
    user_name = input("Enter your name: ")
    file_path = user_name + ".json"
    storage = storage_json.StorageJson(file_path)
    # print(storage)  # @TEST
    # print(type(storage))  # @TEST
    # print(storage.get_file_path())  # @TEST
    run_program(storage)


if __name__ == "__main__":
    main()
