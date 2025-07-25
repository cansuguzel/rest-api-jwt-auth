# REST API with JWT Authentication
This project implements two separate RESTful APIs — one for user management and another for note management — built with Python (Flask) and PostgreSQL. All endpoints are secured using JWT (JSON Web Token) based authentication. User passwords are securely hashed using Werkzeug before storing in the database. Access control and user authorization are enforced via custom decorators (@token_required, @self_access_required, @owner_required) to ensure security across all routes.

# Project Structure
```bash
rest-api-jwt/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── utils/
│   │   └── tokens.py
│   ├── decorators.py
│   └── routes/
│       ├── __init__.py
│       ├── users.py
│       └── notes.py
│
├── create_db.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
``` 
 
# Clone the repository

```bash
git clone https://github.com/cansuguzel/rest-api-jwt-auth.git
cd rest-api-jwt-auth
``` 
# Create a virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate
``` 
# Install dependencies

```bash
pip install -r requirements.txt
``` 
# Configure environment 

If you're using a .env file (recommended), create it in the project root with the following content:
```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_db_name
SECRET_KEY=your_flask_secret
JWT_SECRET_KEY=your_jwt_secret
```
Make sure your .env file is not committed to version control. Add it to .gitignore.

Alternatively, you can directly set these values in config.py, but using .env is more secure and flexible.

# Initialize the database

Make sure PostgreSQL is running, then run:
```bash
python create_db.py
```
# Run the server
```bash
python run.py
```
API will run on: http://127.0.0.1:5000

## Authentication
All protected endpoints require a valid JWT access token.

First, register and log in to receive a token.

In Postman:
- Go to Authorization tab
- Choose Bearer Token
- Paste your token from login response
- Go to Body tab,Select raw,Choose JSON as content type

You can test all endpoints using Postman.

Go to Postman and set the Base URL:
   http://127.0.0.1:5000/api/v1/

# User API Endpoints
`POST /api/v1/users/`
Register a new user

 ```json
{
  "username": "cansu",
  "password": "123456"
}
```
Response:
 ```json
{
  "message": "User created successfully."
}

```
`POST /api/v1/users/login`
Login and get JWT token
 ```json
{
  "username": "cansu",
  "password": "123456"
}
```
Response:
 ```json
{
  "token": "<your-access-token>"
}
```

`GET /api/v1/users/` 
List all users.(requires JWT)

Response:
 ```json
[
  {
    "id": 1,
    "username": "cansu"
  },
  {
    "id": 2,
    "username": "admin"
  }
]
 ```

`GET /api/v1/users/me`
Get your user profile (requires JWT)

Response:
 ```json
{
  "id": 1,
  "username": "cansu"
}
 ```
`PUT /api/v1/users/<user_id> `
Update your own account.

Request: PUT /api/v1/users/1
Body:
 ```json
{
  "username": "cansu_updated",
  "password": "newpass123"
}
 ```
Response:
 ```json
{
  "message": "User updated.",
  "user": {
    "id": 1,
    "username": "cansu_updated"
  }
}
 ```
 `DELETE /api/v1/users/<user_id>`
Delete your own user account.

Request: DELETE /api/v1/users/1
Response:
Status code: 204 No Content

# Notes API Endpoints
`GET /api/v1/notes `
Get your notes.

Response:
 ```json
[
  {
    "id": 1,
    "title": "Shopping List",
    "content": "Milk, Bread, Eggs"
  }
]
 ```
`POST /api/v1/notes`
Add a new note.
Body:
 ```json
{
  "title": "Todo",
  "content": "Finish the project"
}
 ```
Response:
 ```json
{
  "message": "Note added.",
  "note_id": 2
}
 ```
`GET /api/v1/notes/<note_id>`
Get a specific note you own.

Request: GET /api/v1/notes/1
Response:
 ```json
{
  "id": 1,
  "title": "Shopping List",
  "content": "Milk, Bread, Eggs"
}
 ```
`PUT /api/v1/notes/<note_id>`
Update your own note.
Request: PUT /api/v1/notes/1

Body:
 ```json
{
  "title": "Updated List",
  "content": "Milk, Bread, Eggs, Cheese"
}
 ```
Response:
 ```json
{
  "message": "Note updated.",
  "note": {
    "id": 1,
    "title": "Updated List",
    "content": "Milk, Bread, Eggs, Cheese"
  }
}
 ```

`DELETE /api/v1/notes/<note_id>`
Delete your own note.

Request: DELETE /api/v1/notes/1

Response:
Status: 204 No Content

### Postman Collection
A Postman collection file is included in this project for easy API testing.
File:
  Rest API JWT.postman_collection.json

This file contains sample requests for all endpoints, including proper authentication and body examples.

`How to Use`:
 - Open Postman
 - Go to File → Import
 - Select the .json file from this project
 - All requests will be pre-configured, including headers and sample bodies.

## Technologies Used
- Python 
- Flask
- SQLAlchemy
- PostgreSQL
- JWT Authentication (PyJWT)
- Secure password hashing (`werkzeug.security`)
- Postman (for test)

### Database Info
Database: PostgreSQL

DB Name: note_app

Tables: user, note

ORM: SQLAlchemy
### Developer
 Name: Cansu Güzel

 Project: REST API with JWT Authentication

 ### What's Next?
In the next version of this project, I plan to:

- Add **JWT Refresh Token** functionality
- Add admin authorization logic for user management
