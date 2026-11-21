"""
AuthService - handles user login and authentication.

Concepts used:
1. Authentication
2. Password Hashing
3. Classes and Objects
4. Encapsulation
5. Custom Exception Handling
6. Role-Based Access

"""

# We have created a separate AuthService class to keep login separate
#from request management. This follows the Single Responsibilty principle.
import hashlib

from domain.user import User
from domain.exceptions import AuthenticationError

# Authentication : checking whether a user is actually who they claim to be.
# Hashing : Hashing converts the original password into a different fixed-length string.
# Example:  Original password : admin123,  SHA-256 hashing: Password is converted into a hash, Hashed password: A long hexadecimal string

# This function converts a password into a fixed-length hash.
# One way hash : We are comparing password hashes instead of storing plain passwords.
# hashlib: Python's built-in module for hashing.
# sha256(): Applies the SHA-256 hashing algorithm.
# encode("utf-8"): Converts the password string into bytes.
# hexdigest(): Returns the hash as a readable hexadecimal string.
# Hashing is different from encryption. Hashing is designed to be one-way, while encryption can be reversed using the correct key.

def _hash(password):
    
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class AuthService:
    def __init__(self):
        # Store users in a dictionary.
        # Username is the key and (password hash, role) is the value.
        # Example:
        # "admin" -> (hashed password, ADMIN role)
        # "staff" -> (hashed password, STAFF role)
        self.__users = {
            "admin": (_hash("admin123"), User.ROLE_ADMIN),
            "staff": (_hash("staff123"), User.ROLE_STAFF),
        }

    def login(self, username, password):
        """Check the login details and return a User object if valid."""

        # Convert the username to lowercase and remove extra spaces.
        # Then find the user's details in our dictionary.
        # strip() removes extra spaces.
        # lower() converts the username to lowercase.
        # get() searches for the username in the dictionary.
        record = self.__users.get(username.strip().lower())

        # Check two things:
        # 1. Does the username exist?
        # 2. Does the entered password's hash match the stored hash?
        # We have used record[0] Because the dictionary value is a tuple. Index 0 contains the password hash,
        # and index 1 contains the user's role.
        if record is None or record[0] != _hash(password):
            raise AuthenticationError("Invalid username or password.")

        # If the login details are correct, create and return a User object.
         # The user's role is taken from the stored record.
        return User(username.strip().lower(), record[1])
