# Job Tracker API

A RESTful API built with **Python and FastAPI** for managing and tracking job applications.

The project demonstrates backend development concepts including REST APIs, database integration, input validation, dependency injection, error handling, and automated API testing.

## Features

- Create job applications
- View all applications
- View a single application by ID
- Update applications
- Delete applications
- Filter applications by status
- Input validation using Pydantic
- URL validation using `HttpUrl`
- Restricted application statuses
- Empty-field validation
- 404 error handling
- SQLite database with SQLAlchemy ORM
- Dependency injection for database sessions
- Automated API testing with pytest
- Isolated in-memory database for tests
- Interactive Swagger/OpenAPI documentation

## Tech Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **SQLite**
- **Pytest**
- **HTTPX**
- **Uvicorn**

## Project Structure

```text
job-tracker-api/
│
├── main.py              # FastAPI application and API endpoints
├── database.py          # Database configuration
├── models.py            # SQLAlchemy database models
├── test_main.py         # Automated API tests
├── jobtracker.db        # Local SQLite database
├── README.md            # Project documentation
├── .gitignore           # Git ignored files
└── venv/                # Python virtual environment
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/applications` | Get all applications |
| GET | `/applications?status=Applied` | Filter applications by status |
| GET | `/applications/{id}` | Get application by ID |
| POST | `/applications` | Create a new application |
| PUT | `/applications/{id}` | Update an application |
| DELETE | `/applications/{id}` | Delete an application |

## Application Statuses

The API accepts only these application statuses:

```text
Applied
Interview
Rejected
Selected
```

Invalid statuses are rejected automatically by Pydantic validation.

## Example Request

### Create Application

```json
{
  "company": "Google",
  "role": "AI Engineer Intern",
  "status": "Applied",
  "application_date": "2026-10-26",
  "job_link": "https://google.com",
  "notes": "Applied through careers portal"
}
```

## Validation

The API validates incoming data before storing it in the database.

For example:

- Company cannot be empty
- Role cannot be empty
- Application date cannot be empty
- Notes cannot be empty
- Job link must be a valid URL
- Status must be one of the supported values

Invalid requests return:

```text
422 Unprocessable Entity
```

## Error Handling

If an application ID does not exist, the API returns:

```text
404 Not Found
```

with:

```json
{
  "detail": "Application not found"
}
```

## Database

The project uses **SQLite** with **SQLAlchemy ORM**.

The database is created locally as:

```text
jobtracker.db
```

Database sessions are managed using FastAPI dependency injection.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/krishn11x/ledgerpilot.git
```

> Replace the repository URL above with the URL of this Job Tracker API repository if it has a different name.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pytest httpx
```

### 5. Start the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test all API endpoints directly from Swagger UI.

## Running Tests

The project includes automated tests using pytest.

Run:

```powershell
.\venv\Scripts\python.exe -m pytest
```

The test suite covers:

- Root endpoint
- Creating applications
- Retrieving applications
- Updating applications
- Deleting applications
- Invalid input validation

Tests use a separate **in-memory SQLite database**, so running tests does not modify the actual application database.

## Example Workflow

```text
Client / Swagger
       ↓
     FastAPI
       ↓
Pydantic Validation
       ↓
   API Endpoint
       ↓
  SQLAlchemy ORM
       ↓
   SQLite Database
```

## Learning Outcomes

Through this project, I practiced:

- REST API development
- FastAPI
- Pydantic validation
- SQLAlchemy ORM
- SQLite database integration
- Dependency injection
- HTTP status codes
- Error handling
- Automated testing
- Test database isolation
- Git and GitHub workflow

## Future Improvements

Possible future improvements include:

- JWT authentication
- User accounts
- PostgreSQL support
- Pagination
- Sorting and advanced filtering
- Frontend dashboard
- Docker deployment
- Cloud deployment
- Job application analytics

## Author

**Krishna Gupta**

GitHub:  
https://github.com/krishn11x