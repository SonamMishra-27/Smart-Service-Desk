"""
This file contains the ServiceRequest class.
It stores all the details of a service request and handles
the main rules, such as checking priority and resolving a request.
-- Class -> It is a blueprint used to create service request objects.
-- Class Attributes -> They belong to the class and shared by objects.

This is the main class of our Domain layer. 
It represents an individual service request. 
I have used a constructor to initialize the request details and private attributes to demonstrate encapsulation. 
I have used properties to provide read-only access to those attributes. The class also contains methods such as resolve() 
to implement the business rule of changing a request from OPEN to RESOLVED. 
I have also used static methods and class methods for validation and object creation. The to_dict() and from_dict() 
methods help convert objects into dictionaries and restore them from saved JSON data.

This class knows the business rules (valid priority, OPEN -> RESOLVED)
but it knows NOTHING about files, JSON files or the menu.
"""

# Import custom exceptions used for validation and status checking
from domain.exceptions import (
    InvalidPriorityError,
    InvalidInputError,
    AlreadyResolvedError,
)

# Class: A blueprint used to create service request objects
class ServiceRequest:
    # Class attributes: These values are common to all request objects
    # Why use them? Instead of writing "LOW", "MEDIUM", "HIGH" repeatedly 
    # throughout our code, we have defined them once. 
    VALID_PRIORITIES = ("LOW", "MEDIUM", "HIGH")
    STATUS_OPEN = "OPEN"
    STATUS_RESOLVED = "RESOLVED"


    # Constructor: Runs automatically whenever a new object is created
    # Constructor runs when we write ServiceRequest(...).
    # self -> refers to the current object.
    def __init__(self, request_id, employee_name, issue, priority, status=STATUS_OPEN):
        
        
        # ENCAPSULATION: keeping data and the methods that work on that data together,
        # while controlling how the data is accessed or modified.
        # the double underscore makes these attributes PRIVATE and helps
        # protect internal data and we use validation before storing values in the object,
        # so outside code cannot do request.__status = "RESOLVED" directly.
        self.__request_id = self._clean_text(request_id, "Request ID").upper()
        self.__employee_name = self._clean_text(employee_name, "Employee name")
        self.__issue = self._clean_text(issue, "Issue description")
        self.__priority = self._validate_priority(priority)
        self.__status = self._validate_status(status)

    # ---------- PUBLIC read-only access (properties) ----------
    # Properties provide read-only access to our private attributes
    # Other classes can read these values without changing them directly

    # @property allows us to access a method like an attribute.
    @property
    def request_id(self):
        return self.__request_id

    @property
    def employee_name(self):
        return self.__employee_name

    @property
    def issue(self):
        return self.__issue

    @property
    def priority(self):
        return self.__priority

    @property
    def status(self):
        return self.__status

    # ---------- PUBLIC behaviour (methods) ----------
    # Methods are functions defined inside a class.
    # Public methods: These define the actions that can be performed on an object
    

    # resolve() – business logic, It checks whether the request is already resolved.
    # It is kept inside ServiceRequest because changing the request status is a business rule 
    # and the domain layer should control business rules.
    def resolve(self):
        
        # A request can only be resolved if it is not already resolved
        #BUSINESS RULE: OPEN -> RESOLVED.
        #This is the ONLY place where the status is changed.
        
        if self.__status == self.STATUS_RESOLVED:
            raise AlreadyResolvedError(
                f"Request {self.__request_id} is already RESOLVED."
            )
        # Change the status to RESOLVED
        self.__status = self.STATUS_RESOLVED
        return True

    # is_open() : This checks whether the request is OPEN.
    def is_open(self):
        return self.__status == self.STATUS_OPEN

    # to_dict() :converts our Python object into a dictionary.
    # Because JSON stores data in a structured format, 
    # and we need to convert our object into a format that can be saved.
    def to_dict(self):
        #Convert the object to a plain dictionary (so it can be saved as JSON).
        return {
            "request_id": self.__request_id,
            "employee_name": self.__employee_name,
            "issue": self.__issue,
            "priority": self.__priority,
            "status": self.__status,
        }

    # @classmethod : A class method receives the class itself as its first argument, represented by cls.
    # This creates an object with the saved details.
    # When we restart our application, the JSON file contains dictionaries, not actual Python objects.
    # We need to convert those dictionaries back into ServiceRequest objects.
    # That's why we use from_dict().
    @classmethod
    def from_dict(cls, data):
        # Create a new object using the details loaded from the JSON file
        return cls(
            data["request_id"],
            data["employee_name"],
            data["issue"],
            data["priority"],
            data["status"],
        )

    # __str__() : This is a special method in Python.
    # It controls what happens when we print an object.
    def __str__(self):
    
        return (
            f"{self.__request_id} | {self.__employee_name} | {self.__issue} | "
            f"{self.__priority} | {self.__status}"
        )

    # ---------- PRIVATE helper methods (single underscore = internal use) ----------
    # Helper Methods: used internally for checking and cleaning data
    

    # static method : A static method is a method that does not need self or cls.
    # It performs a task using the values passed to it.
    # Here, _clean_text() removes unnecessary spaces and checks whether the entered field is empty.
    @staticmethod
    def _clean_text(value, field_name):
        # Remove extra spaces and make sure the field is not empty.
        text = str(value).strip()
        if not text:
            raise InvalidInputError(f"{field_name} cannot be empty.")
        return text

    @classmethod
    def _validate_priority(cls, priority):
        # DOMAIN VALIDATION: the object can never exist with a wrong priority.
        # Convert priority to uppercase and check if it is valid. If not, raise an exception.
        value = str(priority).strip().upper()
        if value not in cls.VALID_PRIORITIES:
            raise InvalidPriorityError("Priority must be LOW, MEDIUM or HIGH.")
        return value

    @classmethod
    def _validate_status(cls, status):
        # Check whether the status is OPEN or RESOLVED
        value = str(status).strip().upper()
        if value not in (cls.STATUS_OPEN, cls.STATUS_RESOLVED):
            raise InvalidInputError("Status must be OPEN or RESOLVED.")
        return value
