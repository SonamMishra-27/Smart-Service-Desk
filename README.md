# Smart Service Desk Management System

A command-line Python application that helps IT support teams manage employee service requests. Users can create, view, search and resolve requests through a simple menu-driven interface.

The application uses Object-Oriented Programming, a layered architecture and JSON-based file storage. All requests are saved permanently, so the data remains available even after the application is closed and restarted.

---

## 1. Problem Statement

Companies receive different types of IT support requests from employees, such as:

- Laptop and hardware problems
- Software installation issues
- Network connectivity problems
- Password and account issues
- Access and permission-related problems

Managing these requests manually can make it difficult to track their status and maintain records.

The Smart Service Desk Management System provides a simple digital solution to manage these requests. It allows employees and administrators to perform different operations based on their roles.

## 2. Project Objectives

The main objectives of this project are:

1. To provide a simple system for creating and managing IT service requests.
2. To allow users to search and view existing requests.
3. To provide role-based access for administrators and staff.
4. To maintain request information even after the application is closed.
5. To apply OOP, SOLID principles and basic Domain-Driven Design (DDD).
6. To handle invalid inputs and unexpected data-related problems using exception handling.
7. To maintain a structured and maintainable Python project.

## 3. Implemented Features

The application provides the following features:

| Feature | Description |
|---|---|
| User Login | Users log in using their username and password. |
| Role-Based Access | Two roles are available: ADMIN and STAFF. |
| Create Request | Users can create a new service request by entering its ID, employee name, issue and priority. |
| Automatic Status | Every newly created request receives the status `OPEN`. |
| View Requests | Displays all existing service requests. |
| Search Request | Finds a particular request using its Request ID. |
| Resolve Request | Changes the status of an open request to `RESOLVED`. Only ADMIN users can perform this operation. |
| Data Persistence | Saves requests in a JSON file and loads them when the application starts. |
| Error Handling | Displays meaningful error messages for invalid inputs and application-related errors. |

### Request Status Flow

A newly created request starts with the status `OPEN`.

When an administrator resolves it, the status changes to `RESOLVED`.

```text
       Create Request
             |
             v
           OPEN
             |
             | Admin resolves request
             v
         RESOLVED
```

A request that is already resolved cannot be resolved again.

## 4. Login Credentials

The following demo credentials are available in the application:

| Username | Password | Role | Can Resolve Requests? |
|---|---|---|---|
| admin | admin123 | ADMIN | Yes |
| staff | staff123 | STAFF | No |

**Login Rules:**

- The user must enter a valid username and password.
- A maximum of three login attempts is allowed.
- If all three attempts fail, the application exits.
- The ADMIN user can perform all four request operations.
- The STAFF user can create, view and search requests, but cannot resolve them.

## 5. Technologies and Python Modules Used

| Technology / Module | Purpose |
|---|---|
| Python | Main programming language |
| JSON | Stores request information in a structured format |
| `json` | Converts Python data into JSON and reads JSON data |
| `pathlib` | Handles file and folder paths |
| `hashlib` | Generates password hashes using SHA-256 |
| `abc` | Creates an abstract repository class |
| OOP | Organises the application using classes and objects |
| Git and GitHub | Tracks changes and manages branches and commits |

No external Python libraries are required.

## 6. Project Architecture – Layered Architecture and DDD

The project follows a basic Domain-Driven Design (DDD) structure.

The code is divided into four layers. Each layer has a separate responsibility.

### 6.1 Domain Layer

**Folder:** `domain/`

The Domain Layer contains the core classes, business rules and repository contract of the application.

Files:

- `service_request.py`
- `user.py`
- `request_repository.py`
- `exceptions.py`

Responsibilities:

- Defines the ServiceRequest and User classes.
- Stores request and user-related information.
- Validates request details such as priority and status.
- Controls the request status transition from OPEN to RESOLVED.
- Defines custom exceptions.
- Defines the abstract repository contract.

For example, the `ServiceRequest` class contains the `resolve()` method, which changes the request status. This business rule is kept inside the domain class rather than being implemented in the menu.

### 6.2 Application Layer

**Folder:** `application/`

The Application Layer coordinates the operations performed by the user.

Files:

- `request_service.py`
- `auth_service.py`

Responsibilities:

- Creates new service requests.
- Displays and searches existing requests.
- Checks whether a user has permission to resolve a request.
- Handles login and authentication.
- Communicates with the repository to load and save data.

`RequestService` handles the main application use cases, while `AuthService` handles user login.

### 6.3 Infrastructure Layer

**Folder:** `infrastructure/`

The Infrastructure Layer handles technical operations related to data storage.

File:

- `file_repository.py`

Responsibilities:

- Reads request data from the JSON file.
- Converts JSON data into Python objects.
- Converts Python objects into dictionaries.
- Saves updated request information.
- Handles file-related errors and invalid JSON data.

The `FileRepository` class implements the abstract methods defined by `RequestRepository`.

### 6.4 Presentation Layer

**File:** `main.py`

The Presentation Layer is responsible for interacting with the user.

Responsibilities:

- Displays the login screen.
- Takes username and password input.
- Displays the application menu.
- Takes request details from the user.
- Calls the appropriate application service.
- Displays success and error messages.
- Handles menu navigation and application exit.

The presentation layer does not contain the main business rules. It delegates the actual work to the application and domain layers.

### Overall Application Flow

```text
                  USER
                    |
                    v
                main.py
           (Presentation Layer)
                    |
                    v
             RequestService
           (Application Layer)
                    |
                    v
          RequestRepository
             (Abstract Class)
                    |
                    v
             FileRepository
          (Infrastructure Layer)
                    |
                    v
              requests.json
              (Data Storage)
```

The `ServiceRequest` domain class is also used by `RequestService` and `FileRepository` to validate, manage and convert request data.

## 7. Object-Oriented Programming Concepts

The project demonstrates the major concepts of Object-Oriented Programming.

### 7.1 Class and Object

A class is a blueprint used to create objects.

In this project:

- `ServiceRequest` is a class.
- Each service request created by the application is an object of this class.
- `User` is a class.
- Each successfully logged-in user is represented by a User object.

Example:

```python
request = ServiceRequest(
    "SR101",
    "Rahul",
    "Laptop is not working",
    "HIGH"
)
```

Here, `request` is an object of the `ServiceRequest` class.

### 7.2 Constructor

A constructor is a special method called `__init__()`.

It runs automatically when an object is created and initialises its attributes.

Example:

```python
def __init__(self, request_id, employee_name, issue, priority):
    self.__request_id = request_id
```

### 7.3 Attributes

Attributes are variables that store information about an object.

The `ServiceRequest` class contains:

- `request_id`
- `employee_name`
- `issue`
- `priority`
- `status`

### 7.4 Methods

Methods are functions defined inside a class.

Examples from the project:

- `resolve()`
- `is_open()`
- `to_dict()`
- `from_dict()`
- `create_request()`
- `view_requests()`
- `search_request()`
- `resolve_request()`
- `login()`

### 7.5 Encapsulation

Encapsulation means keeping data and the methods that operate on that data together and controlling how that data is accessed or changed.

Example:

```python
self.__status = status
```

The double underscore uses Python's name-mangling mechanism.

The `ServiceRequest` class exposes the status through a read-only property:

```python
@property
def status(self):
    return self.__status
```

The status is changed through the `resolve()` method, which also checks whether the request is already resolved.

This helps protect the object's internal data from accidental changes.

### 7.6 Abstraction

Abstraction means exposing what an object should do without requiring other parts of the application to know its internal implementation.

In this project, `RequestRepository` is an abstract class created using Python's `ABC` module.

It defines two abstract methods:

- `load_all()`
- `save_all()`

The `FileRepository` class implements these methods.

The abstract class defines what operations a repository must provide, while the concrete repository defines how those operations are performed.

## 8. Access Levels in Python

Python uses naming conventions and name mangling to indicate different levels of access.

| Access Level | Syntax | Example |
|---|---|---|
| Public | `name` | `resolve()`, `create_request()`, `request.status` |
| Protected convention | `_name` | `_clean_text()`, `_validate_priority()` |
| Private-style | `__name` | `self.__status`, `self.__repository`, `self.__requests` |

**Note:** Python does not enforce strict private or protected access in the same way as some other languages. A single underscore indicates internal use by convention. A double underscore triggers name mangling.

## 9. Exception Handling

Exception handling is used to manage errors without allowing the application to terminate unexpectedly during normal operations.

### 9.1 Built-in Exceptions

The project uses the following built-in exceptions:

| Exception | Purpose |
|---|---|
| `ValueError` | Handles non-numeric menu input |
| `OSError` | Handles file reading and writing errors |
| `json.JSONDecodeError` | Handles invalid JSON data |
| `KeyError` | Handles missing dictionary keys |
| `TypeError` | Handles incorrect data types |
| `KeyboardInterrupt` | Handles manual program interruption |
| `EOFError` | Handles unexpected end of input |

### 9.2 Custom Exceptions

Custom exceptions are defined in:

`domain/exceptions.py`

Examples:

- `ServiceDeskError`
- `RequestNotFoundError`
- `DuplicateRequestError`
- `InvalidPriorityError`
- `InvalidInputError`
- `AlreadyResolvedError`
- `InvalidMenuChoiceError`
- `AuthenticationError`
- `PermissionDeniedError`
- `DataFileError`

All custom exceptions inherit from the base class `ServiceDeskError`.

This allows the application to catch different application-specific errors using one common exception handler:

```python
except ServiceDeskError as error:
    print(f"Error: {error}")
```

### 9.3 Try, Except and Finally

The project uses:

- `try`: Contains code that may raise an exception.
- `except`: Handles the exception.
- `finally`: Executes after the try/except process finishes.

For example, `main.py` uses a `finally` block to display a session-ending message.

The project also uses `raise` to generate custom exceptions when a business rule is violated.

No bare `except:` block is used.

## 10. File Handling and Data Persistence

The application stores all service requests in:

`data/requests.json`

### 10.1 What is Persistence?

Persistence means saving data permanently so that it remains available even after the program is closed.

For example, if an administrator creates a request and closes the application, the request should still be available when the application is started again.

### 10.2 Saving Data

The `FileRepository` class uses:

```python
json.dump(data, file, indent=4)
```

Before saving, every `ServiceRequest` object is converted into a dictionary using the `to_dict()` method.

The dictionaries are then stored in JSON format.

### 10.3 Loading Data

When the application starts, `RequestService` calls:

```python
self.__repository.load_all()
```

The `FileRepository` class reads the JSON file and converts each dictionary back into a `ServiceRequest` object using:

```python
ServiceRequest.from_dict(item)
```

### 10.4 Handling File Conditions

The application safely handles:

- Missing JSON file: returns an empty list.
- Empty JSON file: returns an empty list.
- Invalid JSON content: raises `DataFileError`.
- Incorrect data format: raises `DataFileError`.
- Invalid request details: raises `DataFileError`.
- File reading or writing problems: raises `DataFileError`.

Data is saved after a successful request creation or resolution.

## 11. SOLID Principles

The project demonstrates two SOLID principles: Single Responsibility Principle and Dependency Inversion Principle.

### 11.1 Single Responsibility Principle (SRP)

A class should have one main responsibility.

Each class in the project has a separate job.

| Component | Main Responsibility |
|---|---|
| `ServiceRequest` | Stores request information and manages request-related business rules |
| `User` | Stores username and role information |
| `RequestRepository` | Defines the abstract contract for loading and saving requests |
| `FileRepository` | Reads and writes JSON data |
| `RequestService` | Handles request-related application operations |
| `AuthService` | Handles user authentication |
| `main.py` | Handles menu, user input and output |

This separation makes the code easier to maintain, understand and modify.

### 11.2 Dependency Inversion Principle (DIP)

High-level modules should depend on abstractions rather than directly depending on low-level implementation details.

In this project:

- `RequestService` depends on the abstract `RequestRepository`.
- It does not directly depend on `FileRepository`.
- `FileRepository` implements the abstract repository contract.
- The actual repository object is created in `main.py` and passed to `RequestService`.

Example:

```python
repository = FileRepository(DATA_FILE)
service = RequestService(repository)
```

This makes it easier to replace JSON storage with another storage method in the future without changing the main request-handling logic, provided the new repository implements the same contract.

## 12. Authentication and Authorization

The project demonstrates both authentication and authorization.

### Authentication

Authentication checks whether the user is valid.

The `AuthService` class:

1. Receives the username and password.
2. Finds the corresponding user record.
3. Hashes the entered password.
4. Compares the entered password's hash with the stored hash.
5. Raises `AuthenticationError` if the credentials are incorrect.
6. Returns a `User` object after successful login.

### Password Hashing

The project uses Python's built-in `hashlib` module and the SHA-256 algorithm.

Passwords are hashed instead of being stored as plain-text values in the user dictionary.

**Security note:** SHA-256 is used here to demonstrate the basic concept of hashing. For a real production application, password-specific algorithms such as Argon2 or bcrypt, with appropriate salting and configuration, should be used. The demo credentials are also hardcoded for this assignment and should not be used in a real system.

### Authorization

Authorization determines which operations a logged-in user is allowed to perform.

The project uses two roles:

- ADMIN
- STAFF

The `RequestService` checks the user's role before allowing a request to be resolved.

Only ADMIN users can resolve requests.

## 13. Git and GitHub

Git is used for version control. It tracks changes made to the project and maintains a history of commits.

The project uses two branches:

### Main Branch

The `main` branch contains the stable and final version of the application.

### Development Branch

The `development` branch is used for making changes and adding features before merging them into `main`.

### Commit History

The following table describes the planned project development history. The actual commit history can be verified using Git commands.

| Commit | Commit Message | Work Completed |
|---|---|---|
| 1 | Initial project structure | Created project folders, `.gitignore` and initial data file |
| 2 | Add ServiceRequest domain model and exceptions | Added domain classes, validation and custom exceptions |
| 3 | Add JSON file repository | Implemented JSON reading and writing |
| 4 | Add request service and login with roles | Added application services and authentication |
| 5 | Complete CLI application | Connected the application using `main.py` |
| 6 | Add detailed README | Documented project features, architecture and concepts |

### Git Workflow Followed

**Step 1: Create the repository**

```bash
git init
git add .
git commit -m "Initial project structure"
```

**Step 2: Create the development branch**

```bash
git checkout -b development
```

**Step 3: Make changes and commit them**

```bash
git add .
git commit -m "Add ServiceRequest domain model and exceptions"
```

Repeat this process as new features are added.

**Step 4: Test the application**

Check the main operations, error handling and data persistence before merging.

**Step 5: Merge development into main**

```bash
git checkout main
git merge development --no-ff -m "Merge development into main"
```

**Step 6: Push changes to GitHub**

```bash
git push -u origin main
git push -u origin development
```

**Step 7: Verify commit history**

```bash
git log --oneline --graph --all
```

### What is Merging?

Merging combines the changes from one branch into another.

In this project, the changes made in `development` are merged into `main` after testing.

The `--no-ff` option creates a merge commit, preserving a visible record of the branch merge.

## 14. Project Folder Structure

```text
smart-service-desk/
|
|-- domain/
|   |-- __init__.py
|   |-- service_request.py
|   |-- user.py
|   |-- request_repository.py
|   |-- exceptions.py
|
|-- application/
|   |-- __init__.py
|   |-- request_service.py
|   |-- auth_service.py
|
|-- infrastructure/
|   |-- __init__.py
|   |-- file_repository.py
|
|-- data/
|   |-- requests.json
|
|-- main.py
|-- README.md
|-- .gitignore
```

### Folder Description

- `domain/`: Contains core classes, business rules, abstract repository and custom exceptions.
- `application/`: Contains application services and use cases.
- `infrastructure/`: Contains JSON file storage implementation.
- `data/`: Stores saved service request information.
- `main.py`: Starts the application and handles user interaction.
- `README.md`: Contains project documentation.
- `.gitignore`: Specifies files and folders that Git should ignore.

## 15. Installation and Execution

### Requirements

- Python 3.8 or newer.
- Git (only needed for version control).
- No external Python packages are required.

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

Replace the placeholder with the actual GitHub repository URL.

### Step 2: Open the Project Folder

```bash
cd smart-service-desk
```

### Step 3: Run the Application

On Windows:

```bash
python main.py
```

On Linux or macOS:

```bash
python3 main.py
```

## 16. Sample Application Run

```text
=== LOGIN ===

Username: admin
Password: admin123

Welcome, admin (ADMIN).

SMART SERVICE DESK SYSTEM
1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit

Enter your choice: 1

Enter Request ID: SR101
Enter Employee Name: Rahul
Enter Issue: Laptop is not starting
Enter Priority: HIGH

Service Request created successfully.
```

The new request is saved in `data/requests.json` with the status `OPEN`.

## 17. Testing Checklist

The following scenarios should be tested before submission.

| Test Case | Expected Result |
|---|---|
| Login using correct ADMIN credentials | Login successful |
| Login using correct STAFF credentials | Login successful |
| Login using incorrect credentials | Error message displayed |
| Enter incorrect login details three times | Application exits |
| Create a request with valid details | Request created successfully |
| Create another request with the same ID | Duplicate request error |
| Enter an invalid priority | Invalid priority error |
| Leave a required field empty | Invalid input error |
| View requests when records exist | All requests displayed |
| View requests when no records exist | No requests found message |
| Search using an existing ID | Matching request displayed |
| Search using an unknown ID | Request not found error |
| Resolve a request as ADMIN | Status changes to RESOLVED |
| Resolve a request as STAFF | Permission denied error |
| Resolve an already resolved request | Already resolved error |
| Enter letters instead of a menu number | Invalid menu choice error |
| Enter a number outside 1–5 | Invalid menu choice error |
| Restart the application after creating a request | Previously saved request is still available |
| Use an invalid JSON file | Data file error displayed |

## 18. Limitations and Future Improvements

The current application is designed as a small command-line assignment project.

Possible future improvements include:

1. **Database Integration:** Replace JSON storage with SQLite, MySQL or PostgreSQL.
2. **Improved Authentication:** Use secure password hashing algorithms such as Argon2 or bcrypt.
3. **User Management:** Allow administrators to add, remove and manage users.
4. **Request Updates:** Allow authorised users to update request details and priorities.
5. **Additional Statuses:** Introduce statuses such as IN_PROGRESS, ON_HOLD and CLOSED.
6. **Graphical Interface:** Develop a web-based or desktop interface.
7. **Automated Testing:** Add unit tests using Python's `unittest` or `pytest`.
8. **Request Tracking:** Add timestamps and maintain a history of request status changes.

## 19. Conclusion

The Smart Service Desk Management System provides a simple way to manage employee IT support requests through a command-line interface.

The project demonstrates practical implementation of Object-Oriented Programming, abstraction, encapsulation, exception handling, JSON file handling, persistence, SOLID principles, basic DDD and Git version control.

By separating the application into different layers and assigning each class a clear responsibility, the project becomes easier to understand, maintain and extend in the future.

## Evaluation Questions:
Why does ServiceRequest belong to Domain? It holds core business data and rules (valid priority, OPEN → RESOLVED) and knows nothing about files or the menu.

Where is the OPEN → RESOLVED rule? In ServiceRequest.resolve(). Everything else calls this method.

Why is JSON handling outside the domain? Single Responsibility. If we switch to a database later, only the infrastructure layer changes. Domain logic never directly opens or updates the file.

Trigger a custom exception: search for SR999. The service raises RequestNotFoundError, and main.py catches it in run_menu with except ServiceDeskError and prints a friendly message.

Dependency Inversion: RequestService depends on the abstract RequestRepository, not on FileRepository. main.py injects the real one.

Persistence: restart the app and search SR101.
Git graph: explain that development holds the work commits and main received them by merge.