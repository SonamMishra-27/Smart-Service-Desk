"""
FileRepository - handles reading and writing data in a JSON file.

Concepts used:
1. File Handling
2. JSON
3. Persistence
4. Inheritance
5. Abstraction
6. Exception Handling
7. DDD Infrastructure Layer
8. SRP (Single Responsibility Principle)

This class is responsible only for storing and retrieving
service request data from the JSON file.
FileRepository - reads and writes the JSON file.

How all the file will work -> main.py(gets input from user) -> RequestService(Handles application operations) -> RequestRepository(Defines the abstract methods) -> FileRepository(Reads and writes the JSON file) -> requests.json(stores the request data permanently)

"""

import json
from pathlib import Path

from domain.request_repository import RequestRepository
from domain.service_request import ServiceRequest
from domain.exceptions import DataFileError, ServiceDeskError

# Repository: acts as a connection between your application and the place where data is stored.
# In this RequestService asks the repository to load or save requests.
# RequestRepository defines what methods a repository must provide.
# FileRepository actually performs the file operations.
# Inheritance: FileRepository inherits from RequestRepository.


# JSON : stands for JavaScript Object Notation. It is a format used to store and exchange data.
# It must provide implementations for load_all() and save_all().
# load_all(): This method reads existing requests from the JSON file.
# save_all(): This method saves all requests into the JSON file.
# json.load(file) : Reads JSON directly from a file, json.loads(string):Converts a JSON string into Python data
# json.dump(data, file): Writes Python data into a JSON file, json.dumps(data) : Converts Python data into a JSON string
# In this i have used json.load() and json.dump() -> laods() Because  first read the file content into a string using file.read(), and then convert that string into Python data.
class FileRepository(RequestRepository):

    def __init__(self, file_path):
        # Store the file path as a Path object.
        # Double underscore indicates an internal attribute.
        self.__file_path = Path(file_path)

    def load_all(self):
        """Read the JSON file and  saved requests and return them as ServiceRequest objects."""

        # Check whether the JSON file exists.
        # If it does not exist, return an empty list.
        
        if not self.__file_path.exists():
            return []

        try:
            # Open the file in read mode.
            # 'with' automatically closes the file after use.
            # encoding="utf-8"	Supports standard text characters
            # strip()	Removes extra spaces and newlines from the beginning and end
            with open(self.__file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
        
        # Handle errors that occur while reading the file.
        except OSError:
            raise DataFileError("Could not read the data file.")

        # If the file is empty, return an empty list.
        if content == "":
            return []

        try:
            # Convert JSON text into Python data (list/dictionary).
            raw_data = json.loads(content)

        # Handle invalid or corrupted JSON data.
        except json.JSONDecodeError:
            raise DataFileError("The data file is corrupted (invalid JSON).")

        # Our JSON file should contain a list of requests.
        # If it contains something else, raise an error.
        if not isinstance(raw_data, list):
            raise DataFileError("The data file has the wrong format.")

        # Convert every dictionary back into a ServiceRequest object.
        requests = []
        
        for item in raw_data:
            try:
                # from_dict() creates a ServiceRequest object
                # using the details stored in the dictionary.
                # This uses the from_dict() class method from your service_request.py file.
                # It converts each dictionary into a ServiceRequest object.
                requests.append(ServiceRequest.from_dict(item))

            # Handle missing fields, incorrect data types
            # and invalid request details.
            except (KeyError, TypeError, ServiceDeskError):
                raise DataFileError("The data file contains an invalid request.")

        # Return all the loaded ServiceRequest objects.
        return requests

    def save_all(self, requests):
        """Write/Save  all ServiceRequest objects to the JSON file."""

        # Convert every ServiceRequest object into a dictionary.
        # JSON can store dictionaries and lists, not Python objects directly.
        data = [request.to_dict() for request in requests]

        try:
            # Create the data/ folder if it does not exist yet.
            # parents=True: Creates missing parent folders too.
            # exist_ok=True: Does not raise an error if the folder already exists.
            self.__file_path.parent.mkdir(parents=True, exist_ok=True)

            # Open the file in write mode.
            # Write the request data in JSON format.
            # json.dump() writes Python data into a JSON file.
            # indent=4 makes the JSON file properly formatted and easier to read.
            with open(self.__file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

        # Handle errors that occur while writing the file.
        except OSError:
            raise DataFileError("Could not save the data file.")
