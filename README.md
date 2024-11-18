# Secure-Marksheet-System

This system allows users (students, faculty, and admins) to securely upload and download documents, with encrypted file storage and JWT-based authentication. The system uses Flask for the backend, SQLAlchemy for database management, and Flask-JWT-Extended for handling JWT tokens. It also incorporates role-based access control (RBAC) to limit access based on user roles.

Table of Contents
Project Setup
API Endpoints
User Registration
User Login
Upload Document
Get User Documents
Download Document
Admin Route
Postman Collection
Project Setup
Clone the repository:

bash
Copy code
git clone <repo-url>
cd <repo-directory>
Install dependencies:

Ensure you have Python 3.x installed.
Install the required Python packages using pip:
Copy code
pip install -r requirements.txt
Set up the database:

The application uses SQLite for database management. To initialize the database and create the necessary tables, run the following command:
arduino
Copy code
flask run
Configuration:

Modify config.py to use your preferred database and JWT secret key.
python
Copy code
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///documents.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_secret_key'  # Replace with a secure key
Run the Flask application:

Start the application:
arduino
Copy code
flask run
By default, the application will run on http://127.0.0.1:5000/.
API Endpoints
User Registration
POST /register
Allows a user to register by providing a username, password, and role (student, faculty, or admin).

Request Body:

json
Copy code
{
  "username": "john_doe",
  "password": "password123",
  "role": "student"
}
Response:

Success: 201
Failure: 400 (if data is missing or user already exists)
User Login
POST /login
Allows a user to login by providing username and password. Upon successful authentication, an access token is returned.

Request Body:

json
Copy code
{
  "username": "john_doe",
  "password": "password123"
}
Response:

Success: 200 (JWT token)
Failure: 401 (invalid credentials)
Upload Document
POST /upload
Allows faculty and admin users to upload documents. The document will be encrypted before being stored in the database.

Request Body (Form data):

file: The document to be uploaded.
Headers:

Authorization: Bearer <JWT_token>
Response:

Success: 201 (Document uploaded with document ID)
Failure: 403 (if role is not faculty)
Failure: 400 (if no file is provided)
Get User Documents
GET /my-documents
Returns a list of documents that the current user (student) owns.

Headers:

Authorization: Bearer <JWT_token>
Response:

Success: 200 (List of documents with IDs and filenames)
Failure: 401 (if not authenticated)
Download Document
GET /download/<doc_id>
Allows a user to download a document. Only the owner of the document, faculty, and admin users can download it.

Request Parameters:

doc_id: The ID of the document.
Headers:

Authorization: Bearer <JWT_token>
Response:

Success: 200 (Document file)
Failure: 403 (if the user does not have permission)
Failure: 404 (if the document is not found)
Failure: 400 (if file integrity check fails)
Admin Route
GET /admin-only
Only accessible to admin users.

Headers:

Authorization: Bearer <JWT_token>
Response:

Success: 200 (Welcome message)
Failure: 403 (if user is not an admin)
Postman Collection
You can use this Postman collection to test the API endpoints.

Steps to use Postman:
Import the Postman Collection:

Download the Postman collection file.
Open Postman and import the file.
Set the Authorization:

Use the Authorization tab in Postman to set the Bearer Token (JWT) for any endpoints that require authentication.
Test Endpoints:

Use the appropriate HTTP method (POST, GET) and send the required data to test the different routes.
