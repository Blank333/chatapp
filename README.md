# Django Chat App

A chat application built with Django, which allows users to engage in instant messaging with each other.

## Features

- **User Authentication**: Users can create accounts and log in securely.
- **User Profiles**: Users have profiles with their names, emails, and interests.
- **Friend Recommendations**: Recommends friends based on similar interests and preferences.
- **Online Status**: Tracks and displays online status of users.
- **Message History**: Users can view their chat history with other users.

## Setup Instructions

### Installation

1. Clone the repository:

```bash
git clone git@github.com:Blank333/chatapp.git
cd chat-app
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate (Linux/macOS)
env\Scripts\activate (Windows)
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

### Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

### Testing the Application

You can run the unit tests for the application components:

```bash
python manage.py test
```

### API Endpoints

1. **`api/register/`**

   - **Method**: POST
   - **Description**: Allows users to register a new account.
   - **Usage**: Send a POST request with user registration data including email, password, name, age, and interests.
   - **Sample curl request**
     ```bash
     curl --location 'localhost:8000/api/register/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
        "email": "test@example.com",
        "age": 23,
        "name": "TestUser",
        "password": "testingpassword",
        "interests": [
          {
            "name":  "dancing",
            "preference_score": 44
          },
          {
            "name":  "cars",
            "preference_score": 88
          },
          {
            "name":  "travelling",
            "preference_score": 22
          }

        ]
      }
      '
     ```

2. **`api/login/`**

   - **Method**: POST
   - **Description**: Allows users to log in to their existing account and go online.
   - **Usage**: Send a POST request with user login credentials (email and password).
   - **Sample curl request**
     ```bash
     curl --location 'localhost:8000/api/login/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "email": "test@example.com",
          "password": "testingpassword"
      }'
     ```

3. **`api/online-users/`**

   - **Method**: GET
   - **Description**: Retrieves a list of online users.
   - **Usage**: Send a GET request to get a list of users who are currently online.
   - **Sample curl request**
     ```bash
     curl --location 'localhost:8000/api/online-users/'
     ```

4. **`suggested-friends/<int:user_id>/`**

   - **Method**: GET
   - **Description**: Provides a list of suggested friends for a specific user based on shared interests.
   - **Usage**: Send a GET request with the `user_id` parameter to get a list of recommended friends.
   - **Sample curl request**
     ```bash
     curl --location 'localhost:8000/api/suggested-friends/1'
     ```

5. **`start/`**
   - **Method**: POST
   - **Description**: Initiates a chat session between two users. Needs authentication.
   - **Usage**: Send a POST request with data including the email addresses of the users involved.
   - **Sample curl request**
     ```bash
     curl --location 'localhost:8000/api/chat/start/' \
      --header 'Authorization: Token 01592049a859acdde8cb6940f2d1c01e75ab5324' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "recipient_email": "test@example.com"
      }'
     ```
