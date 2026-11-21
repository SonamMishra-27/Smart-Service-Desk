"""
main.py - the PRESENTATION layer.

Concepts used:
1. Functions and Function Calling
2. User Input and Output
3. Conditional Statements and Loops
4. Exception Handling
5. Dependency Injection
6. DDD Presentation Layer

This file interacts with the user through the menu.
It takes input, displays output and calls the required services.
The actual business logic is handled by other classes.

"""

# Presentation layer: Takes input and displays output.
# Dependency Injection : We create an object of FileRepository, We pass that object to RequestService, RequestService uses the repository to load and save requests
# This is called Dependency Injection because an object receives the dependency it needs from outside instead of creating that dependency itself.
# We hav separate functions for each task Because each function handles a particular task. This makes the code easier to read, understand, test and maintain.
# Why to catch ServiceDeskError : All  custom exceptions inherit from ServiceDeskError.
# Therefore, catching ServiceDeskError also catches its child exceptions. This is called exception inheritance.
# It saves us from writing a separate except block for every custom exception.

from pathlib import Path

# Import the application layer classes.
from application.request_service import RequestService
from application.auth_service import AuthService

# Import the infrastructure layer class.
from infrastructure.file_repository import FileRepository
from domain.exceptions import (
    ServiceDeskError,
    InvalidMenuChoiceError,
    AuthenticationError,
    DataFileError,
)

# Find the location of this main.py file.
# Store the JSON file inside the project's data folder.
# Path(__file__).parent: __file__ gives the location of the current Python file.
# -> .parent gives its parent folder.
# / "data" / "requests.json" builds the path to the JSON file. This makes the project less dependent on the folder from which I  run the Python command. 
DATA_FILE = Path(__file__).parent / "data" / "requests.json"

# Maximum number of incorrect login attempts allowed.
MAX_LOGIN_ATTEMPTS = 3


def login(auth_service):
    """ Ask the user to log in (max 3 tries). Return a User object if successful"""
    print("=== LOGIN ===")

    # Allow the user to enter login details up to 3 times.
    for _ in range(MAX_LOGIN_ATTEMPTS):
        username = input("Username: ")
        password = input("Password: ")

        try:
            # Ask AuthService to check the username and password.
            user = auth_service.login(username, password)

            # If login is successful, display a welcome message.
            print(f"Welcome, {user.username} ({user.role}).")
            return user

        # If login details are incorrect, display an error.
        except AuthenticationError as error:
            print(f"Error: {error}")

    # This message is displayed if all 3 attempts fail.
    print("Too many failed attempts. Exiting.")
    return None


def show_menu():
    """Display the main menu of the application."""

    print("\nSMART SERVICE DESK SYSTEM")
    print("1. Create Service Request")
    print("2. View All Requests")
    print("3. Search Request")
    print("4. Resolve Request")
    print("5. Exit")


def read_choice():
    """Read the user's menu choice and check whether it is valid.(INVALID MENU INPUT handling)."""
    
    choice = input("Enter your choice: ").strip()

    # BUILT-IN EXCEPTION: int("abc") raises ValueError in Python.
    # We catch it and convert it into our own CUSTOM exception.
    try:
        # Convert the entered text into an integer.
        # If the user enters something like 'abc',
        # Python raises the built-in ValueError.
        number = int(choice)

    # Catch the built-in error and raise our custom exception.
    except ValueError:
        raise InvalidMenuChoiceError("Invalid choice. Please enter a number from 1 to 5.")

    # Check whether the number is between 1 and 5.
    if number < 1 or number > 5:
        raise InvalidMenuChoiceError("Invalid choice. Please enter a number from 1 to 5.")
    return number


def create_request(service):

    """Take request details from the user and create a request."""

    request_id = input("Enter Request ID: ")
    name = input("Enter Employee Name: ")
    issue = input("Enter Issue: ")
    priority = input("Enter Priority: ")

    # Send the entered details to RequestService.
    service.create_request(request_id, name, issue, priority)

    print("Service Request created successfully.")


def view_requests(service):
    """Display all existing service requests."""

    # Get all requests from RequestService.
    requests = service.view_requests()

    # If there are no requests, display a message and stop this function.
    if not requests:
        print("No service requests found.")
        return

    # Display each request one by one.
    for request in requests:
        print(request)


def search_request(service):
    """Search for a request using its Request ID."""

    request_id = input("Enter Request ID: ")

    # Ask RequestService to find the matching request.
    request = service.search_request(request_id)

    # Display the details of the found request.
    print("\n--- Request Details ---")
    print(f"Request ID  : {request.request_id}")
    print(f"Employee    : {request.employee_name}")
    print(f"Issue       : {request.issue}")
    print(f"Priority    : {request.priority}")
    print(f"Status      : {request.status}")


def resolve_request(service, user):
    """Resolve a request after checking the user's permissions."""

    request_id = input("Enter Request ID: ")

    # RequestService checks whether the user is an ADMIN.
    # If allowed, it changes the request status to RESOLVED.
    request = service.resolve_request(request_id, user)

    print(f"Request {request.request_id} resolved successfully.")


def run_menu(service, user):
    """Keep displaying the menu until the user chooses to exit."""
    while True:
        show_menu()
        try:
            # Read and validate the user's choice.
            choice = read_choice()

            # Call the correct function according to the choice.
            if choice == 1:
                create_request(service)

            elif choice == 2:
                view_requests(service)

            elif choice == 3:
                search_request(service)

            elif choice == 4:
                resolve_request(service, user)

            else:
                # Option 5 exits the menu loop.
                print("Thank you. Goodbye!")
                break

        # Catch expected custom errors and display their messages.
        # This prevents normal application errors from crashing the menu.
        except ServiceDeskError as error:
            # Catches our custom exceptions only (not a bare except).
            print(f"Error: {error}")


def main():
    """Starting point of the complete application."""
    # DEPENDENCY INJECTION:
    # Create the repository object and pass it to RequestService.
    # RequestService does not create FileRepository by itself.
    # Wiring everything together (this is where DEPENDENCY INJECTION happens).
    repository = FileRepository(DATA_FILE)

    try:
        # Create the service object.
        # It loads existing requests through the repository.
        service = RequestService(repository)

    # Handle errors related to loading the JSON file.
    except DataFileError as error:
        print(f"Error: {error}")
        return

    # Create AuthService and ask the user to log in.
    user = login(AuthService())

    # If login fails after 3 attempts, stop the program.
    if user is None:
        return

    # try / except / finally:
    #   try     -> run the application
    #   except  -> handle built-in errors (Ctrl+C or closed input)
    #   finally -> ALWAYS runs, whether the app ended normally or with an error
    try:
        # Start the main menu after successful login.
        run_menu(service, user)

    # Handle cases where the user interrupts or closes input.
    # KeyboardInterrupt: Occurs when the user interrupts the program, commonly by pressing Ctrl + C.
    # EOFError: Can occur when the input stream ends unexpectedly, such as when the user sends an end-of-input signal.
    # Both are built-in Python exceptions.
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
    
    finally:
        # This block runs after the try block finishes,
        # whether the program exits normally or due to these errors.
        print(f"Session ended for {user.username}. All saved data is in data/requests.json.")

# This condition checks whether this file is being run directly.
# If yes, start the application by calling main().
# In Python, __name__ is a special variable.
# If we run a Python file directly, its __name__ becomes "__main__".
# If another file imports it, its __name__ becomes the module's name.
if __name__ == "__main__":
    main()
