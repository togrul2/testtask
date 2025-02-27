# Test application

This project is a sample FastAPI webapp built for test task.

## Features

- **User Signup & Login:**
    - **signup:** Register a new user with a unique username and email.
    - **login:** Authenticate a user with their username and password.

- **Post Management:**
    - **Add Post:** Create posts with a text payload (up to 1MB).
    - **Get Posts:** Retrieve all posts for the authenticated user with in-memory caching (5 minutes).
    - **Delete Post:** Remove a post by its ID if it belongs to the user.

- **Environment Configuration:**  
  Uses environment variables for sensitive settings:
    - `JWT_SECRET_KEY`: The secret key for encoding JWT tokens.
    - `DATABASE_URL`: The connection string for the MySQL database.

## Prerequisites

- Python 3.12+
- MySQL Server (or compatible database like aurora db) running

## Setup and Installation

1. **Set up the app:**

   ```bash
   # Clone the repository.
   git clone https://github.com/togrul2/testtask.git
   cd testtask
   
    # Create a virtual environment.
    python3 -m venv venv
    source venv/bin/activate
    
    # Install the requirements.
    pip install -r requirements.txt

    # Set environment variables.
    export DATABASE_URL=mysql://user:password@localhost/dbname
    export JWT_SECRET_KEY=your_secret_key
    ```

2. **Run the application:**

  ```bash
     python main.py
  ```

or

  ```bash
      uvicorn main:app --reload --host 127.0.0.1 --port 8000
  ```
   
