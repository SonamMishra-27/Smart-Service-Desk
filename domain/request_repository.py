"""
This file contains the abstract RequestRepository class.

It defines which operations a repository must provide,
but does not define how those operations will be performed.

This helps us separate business logic from data storage.
The actual file handling is implemented in the Infrastructure layer.

I have created an abstract class called RequestRepository in my Domain layer. 
It defines two abstract methods, load_all() and save_all(), which every repository implementation must provide. 
I have used Python's ABC module and the abstractmethod decorator to implement abstraction. 
The main purpose is to separate the application logic from the storage implementation. 
My application does not need to know whether the data is stored in JSON or a database. 
This also supports the Dependency Inversion Principle because the application depends on an abstraction rather than a specific storage class.

"""

# Abstraction : Abstraction means hiding the internal implementation and showing only the necessary operations.
# Suppose we want to save service requests. We only need to know load_all() and save_all() -> 
# Do we need to know whether the data is saved in json, mysql or another database -> No we only need to know that these operations are available. 
# That's exactly what abstraction does.

# So how does abstraction works - RquestRepository(Abstract Class) -> defines the required operations(load_all() . save_all())
# -> Inheritance and Implementation -> FileRepository(concrete class) -> Implements actual operations(Reads and writes JSON file).

# Dependency Inversion Principle(DIP) : High-level modules should not depend directly on low-level modules. Both should depend on abstractions.
# Without DIP : RequestService -> FileRepository ->RequestService directly depends on FileRepository
# If tomorrow we want to use MySQL instead of JSON, we may need to change the application code.
# With DIP : RequestService -> RequestRepository(Abstraction) -> FileRepository 
# Now RequestService depends on the abstract repository, not on a specific storage implementation.

# ABC stands for Abstract Base Class. It is used to create an abstract class.
# abstractmethod is a decorator used to define methods that must be implemented by child classes.
from abc import ABC, abstractmethod

# Abstract class: Defines the common structure for all repositories
# By inheriting from ABC, we make RequestRepository an abstract base class.
# We cannot directly create an object of this class because it contains abstract methods that have not been implemented.
class RequestRepository(ABC):

    # Abstract method: Child classes must provide their own implementation
    
    #Return a list of ServiceRequest objects."""
    @abstractmethod
    def load_all(self):
        pass

    # Save a list of ServiceRequest objects.
    @abstractmethod
    def save_all(self, requests):
        pass
