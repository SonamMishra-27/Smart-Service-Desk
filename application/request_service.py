"""
RequestService - handles the main operations of the application.

Concepts used:
1. SRP (Single Responsibility Principle)
2. DIP (Dependency Inversion Principle)
3. DDD Application Layer
4. Encapsulation
5. Custom Exception Handling

This class handles application operations such as creating,
viewing, searching and resolving service requests.

"""

from domain.service_request import ServiceRequest
from domain.request_repository import RequestRepository
from domain.exceptions import (
    DuplicateRequestError,
    RequestNotFoundError,
    PermissionDeniedError,
)

# SRP (Single Responsibility Principle): A class should have one main responsibility.
# RequestService follows SRP because it handles application use cases, while file storage and business rules are handled by separate classes.

# DIP(Dependency Inversion Principle): high-level classes should depend on abstractions, not directly on low-level implementation classes. 
# Here, RequestService depends on RequestRepository rather than FileRepository.
# We are accepting a RequestRepository object from outside. We are not writing: self.__repository = FileRepository() Why?
# Because then RequestService would be directly dependent on the file-storage class.
# Instead, it depends on the abstract RequestRepository class.

# How the classes are connected : Request Service -> RequestRepository(Abstract Class) -> File Repository.

# DDD - Application Layer : RequestService belongs to the application layer because it coordinates the operations using domain objects and the repository.
# We have Three custom exceptions -> DuplicateRequestError, RequestNotFoundError, PermissionDeniedError
# These exceptions are defined separately in domain/exceptions.py and raised here when the relevant condition occurs.

class RequestService:

    def __init__(self, repository: RequestRepository):
        # DEPENDENCY INVERSION: we receive the repository from outside (main.py)
        # and depend on the abstract type, not on FileRepository directly.
        # # This makes our code independent of the storage method.
        self.__repository = repository

        # Encapsulation: This dictionary stores all requests.
        # Load existing requests when the program starts (persistence).
        # A dictionary gives fast lookup by Request ID.
        self.__requests = {}

        # Load previously saved requests when the application starts.
        for request in self.__repository.load_all():
            self.__requests[request.request_id] = request

    def create_request(self, request_id, employee_name, issue, priority):
        """Use case 1: create a new service request (status is automatically OPEN)."""
        # Create a ServiceRequest object. Its constructor checks whether the entered details are valid.
        new_request = ServiceRequest(request_id, employee_name, issue, priority)

        # BUSINESS RULE: same Request ID cannot be created twice.
        # Check whether this request ID already exists.
        if new_request.request_id in self.__requests:
            raise DuplicateRequestError(
                f"Request ID {new_request.request_id} already exists."
            )

        # Add the new request to our dictionary.
        self.__requests[new_request.request_id] = new_request

        # Save the updated requests to the JSON file.
        self.__save()
        return new_request

    def view_requests(self):
        """Use case 2: return all servicerequests."""

        # Convert dictionary values into a list and return them.
        return list(self.__requests.values())

    def search_request(self, request_id):
        """Use case 3: Search for a request using its Request ID."""
        # Remove extra spaces and convert the ID to uppercase.
        key = str(request_id).strip().upper()

        # If the ID is not present, raise a custom exception.
        if key not in self.__requests:
            raise RequestNotFoundError(f"Request {key} not found.")

        # Return the matching request object.
        return self.__requests[key]

    def resolve_request(self, request_id, user):
        """Use case 4: resolve an open request. Only an ADMIN is allowed to do this."""
        
        # Permission check comes first. Check the user's role before allowing the operation.
        if not user.is_admin():
            raise PermissionDeniedError("Only an admin can resolve requests.")

        # Find the request using its ID.
        request = self.search_request(request_id)

        # Change its status from OPEN to RESOLVED.
        # The actual status-changing rule is inside ServiceRequest.
        request.resolve() 

        # Save the updated status to the JSON file.
        self.__save()          
        return request

    def __save(self):
        # Private helper method
        # It sends all current requests to the repository for saving.
        self.__repository.save_all(list(self.__requests.values()))
