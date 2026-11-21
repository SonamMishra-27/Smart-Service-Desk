"""
So what is custom exceptions?
--Python already provides built-in exceptions such as ValueError, TypeError, and FileNotFoundError.
--But sometimes we want to create our own exceptions according to our application's requirements.
--For example, if someone enters an already existing Request ID, we want to raise:
--raise DuplicateRequestError("Request ID already exists")

This file contains all the custom exceptions used in our Smart Service Desk application. 
Instead of using Python's built-in exceptions for every business-related error, I created 
custom exceptions according to the application's requirements. I also created a common parent class
called ServiceDeskError, from which all other custom exceptions inherit. This makes exception 
handling easier because I can catch all application-specific errors using one parent exception

Every exception below inherits from one base class (ServiceDeskError),
so main.py can catch "all expected business errors" with a single
specific except block instead of using a risky bare `except:`.
"""


# Parent exception class for all errors in our application
class ServiceDeskError(Exception):
    # pass means we are not adding anything extra to this class or it means do nothing.
    # We are creating separate exception classes, but we don't need to write any additional implementation inside them.
    # Python already provides the exception behaviour through inheritance.
    pass


# Raised when the entered Request ID does not exist
# Here, RequestNotFoundError inherits from ServiceDeskError. 
#The benefit is that we can handle all our custom application errors together
class RequestNotFoundError(ServiceDeskError):
    pass

# Raised when a user tries to create a Request ID that already exists
class DuplicateRequestError(ServiceDeskError):
    pass

# Raised when the entered priority is not LOW, MEDIUM or HIGH
class InvalidPriorityError(ServiceDeskError):
    pass

# Raised when the user leaves a required field empty
class InvalidInputError(ServiceDeskError):
    pass

# Raised when someone tries to resolve an already resolved request
class AlreadyResolvedError(ServiceDeskError):
    pass

# Raised when the user enters an invalid menu option
class InvalidMenuChoiceError(ServiceDeskError):
    pass

# Raised when the entered username or password is incorrect
class AuthenticationError(ServiceDeskError):
    pass

# Raised when a user tries to perform an action without permission
class PermissionDeniedError(ServiceDeskError):
    pass

# Raised when there is a problem reading or processing the JSON file
class DataFileError(ServiceDeskError):
    pass
