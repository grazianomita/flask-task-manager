# Flask Task Manager

A simple Flask application built with Flask-RestX where authorized users can create/get/delete tasks.
Despite being simple, such application follows best practices that can easily be generalized:

- **Modular structure**: code is packed into separate submodules. A blueprint is used even if not strictly required. 
  Repository classes make the api interact with the database models.
- **Configuration management**: environment variables are stored in a `.env` file and loaded via `load_dotenv()`, 
  ensuring that sensitive information like database credentials or API keys is not hard-coded in your codebase.
- **App Factory Pattern**: Application is initialized using the app factory pattern.
- **Use of Flask Extensions**: Flask extensions are used for common tasks such as:
  - **Database Management** (*Flask-SQLAlchemy*),
  - **Database Migrations** (*Flask-Migrate*)
  - **Authentication** (*Flask-JWT*), 
  - **Serialization** (*Flask-RestX*),
  - **Setting request limits** (*Flask-Limiter*)
- **Input Validation and Serialization**: More specifically, Flask-RestX is used for input validation and 
  serialization, ensuring API endpoints handle input data safely and return well-structured responses.
- **Error Handling**: returning meaningful error messages and appropriate HTTP status codes for different scenarios.
- **Logging**: to collect useful information for debugging purposes and error investigation.
- **Testing**: tests are written using pytest. A pytest-coverage report can evenutually be generated.
- **Documentation**: API endpoints, request/response formats, and authentication mechanisms are documented with minimum 
  effort thanks to the Swagger integration.

## Getting Started

### Prerequisites

- Python 3.6+
- Pip (Python package manager)

### Installation

1. Clone the repository:

   ```bash
   foo@bar:~$ git clone https://github.com/grazianomita/flask_task_manager.git
   foo@bar:~$ cd flask_task_manager
   ```

2. Create a virtual environment and activate it:

   ```bash
   foo@bar:~$ python3 -m venv venv
   foo@bar:~$ source venv/bin/activate  # Linux/macOS
   # Or, for Windows:
   # venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   foo@bar:~$ pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and define the environment variables:

   ```plaintext
   # Add environment variables as needed
   FLASK_ENV=DEV
   FLASK_PORT=5000
   JWT_SECRET_KEY=<YOUR_SECRET_KEY>
   SQLALCHEMY_DATABASE_URI=<YOUR_DB_URI>
   INIT_DATABASE=True
   ```

### Running the Application

To run the application, execute the following command:

```bash
foo@bar:~$ python run.py
```

The application will be accessible by default at `http://127.0.0.1:5000`.

### Running Tests

To run tests using pytest be sure you are in the root directory of the project and execute:

```bash
foo@bar:~$ pytest
foo@bar:~$ pytest --cov=. --cov-report=html
```

## Usage

### Endpoints

- `GET /`: API documentation.
- `POST /api/register`: Endpoint to register new users.
- `POST /api/login`: Endpoint to authenticate users and receive a JWT access and refresh token.
- `POST /api/refresh`: Endpoint to receive a newt JWT access token.
- `GET /api/tasks`: Endpoint to retrieve all tasks.
- `GET /api/tasks/<task_id>`: Endpoint to retrieve a specific task.
- `POST /api/tasks`: Endpoint to create a new task.
- `PUT /api/tasks/<task_id>`: Endpoint to update an existing task.
- `DELETE /api/tasks/<task_id>`: Endpoint to delete a task.
- `DELETE /api/tasks`: Endpoint to delete all tasks.

### Authentication

Protected endpoints (e.g., creating, updating, or deleting tasks) require a valid JWT access token.
The access token must be passed within the authentication header

### Curl Examples

```bash
foo@bar:~$ curl -X POST -H "Content-Type: application/json" -d '{"username": "user", "password": "Passw0rd!"}' http://127.0.0.1:5000/api/register
foo@bar:~$ curl -X POST -H "Content-Type: application/json" -d '{"username": "user", "password": "Passw0rd!"}' http://127.0.0.1:5000/api/login
foo@bar:~$ curl -X POST -H "Authorization: Bearer $jwt_refresh_token" http://localhost:5000/api/refresh
foo@bar:~$ curl -X GET -H "Authorization: Bearer $jwt_access_token" http://127.0.0.1:5000/api/tasks
foo@bar:~$ curl -X GET -H "Authorization: Bearer $jwt_access_token" http://127.0.0.1:5000/api/tasks/1
foo@bar:~$ curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $jwt_access_token" -d '{"name": "task", "priority": 1}' http://127.0.0.1:5000/api/tasks
foo@bar:~$ curl -X PUT -H "Content-Type: application/json" -d '{"task": "updated task", "priority": 2}' http://127.0.0.1:5000/api/tasks/1
foo@bar:~$ curl -X DELETE -H "Authorization: Bearer $jwt_access_token" http://127.0.0.1:5000/api/tasks/1
foo@bar:~$ curl -X DELETE -H "Authorization: Bearer $jwt_access_token" http://127.0.0.1:5000/api/tasks
```


## Additional important points outside the scope of this project

- Replace the Flask development server with a production-ready server like gunicorn for production use.
- Caching, load balancing, database optimization should be considered for production use.
- Implementing rate limiting using Flask-Limiter helps prevent abuse and ensures the stability and availability of your API.
  For production use, a proper storage database should be used for tracking rate limits.
- Proper error handling with meaningful error messages can enhance the user experience and aid in debugging.
- Use HTTPS for secure communication between the client and the server to protect sensitive data.
- Implement input validation and data sanitization to prevent security vulnerabilities such as SQL injection or cross-site scripting (XSS) attacks.
- Consider implementing user roles and permissions for fine-grained access control to API endpoints.