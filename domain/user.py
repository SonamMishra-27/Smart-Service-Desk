"""

This file contains the User class.

It stores user details and checks the user's role.
Our application has two roles:
ADMIN - Can resolve service requests.
STAFF - Can view and manage requests but cannot resolve them.

I have created a User class in the Domain layer to represent users of our application. 
It has two roles, ADMIN and STAFF, defined as class attributes. 
I have used a constructor to initialize the username and role. 
The attributes are private to demonstrate encapsulation, and I have used properties to provide read-only access.
I have also created an is_admin() method that checks whether the current user has administrator privileges. 
This method is used in our role-based access control.

"""

# Class: Blueprint for creating user objects
class User:
    # Class attributes: These roles are common to all User objects
    ROLE_ADMIN = "ADMIN"
    ROLE_STAFF = "STAFF"

     # Constructor: Runs automatically when a new user object is created
    def __init__(self, username, role):

        # Check whether the role is valid
        if role not in (self.ROLE_ADMIN, self.ROLE_STAFF):
            raise ValueError("Role must be ADMIN or STAFF.")

        # Private attributes: Store user details inside the object
        self.__username = username
        self.__role = role

    # Property: Allows other classes to read the username
    # without directly accessing the private attribute
    @property
    def username(self):
        return self.__username

    # Property: Allows other classes to read the user's role
    @property
    def role(self):
        return self.__role

    # Public method: Checks whether the current user has ADMIN role
    def is_admin(self):
        return self.__role == self.ROLE_ADMIN
