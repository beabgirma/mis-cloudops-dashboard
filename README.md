# MIS CloudOps Dashboard

A FastAPI backend project for tracking internal services and their current status.

This project is built like a small backend system for an MIS/cloud operations team. It allows users to create services, view services, update service status, get a service by ID, and delete services.

---

## Project Overview

The goal of this project is to practice building a clean backend API with a professional project structure.

Instead of putting all the logic in one file, the project is organized into layers:

```text
routers/        -> API endpoints
services/       -> business logic
repositories/   -> data storage logic
schemas/        -> request validation
database.py     -> SQLite database setup
tests/          -> automated tests
```

This makes the project easier to grow, test, and maintain.

---

## Features

* Create a service
* List all services
* Get one service by ID
* Update a service status
* Delete a service by ID
* Store services in SQLite
* Track when services are created and updated
* Validate allowed status values
* Return 404 errors when a service does not exist
* Run the app with Docker
* Automated tests with Pytest
* GitHub Actions workflow for running tests on pull requests

---

## Tech Stack

* Python
* FastAPI
* Pydantic
* SQLite
* Pytest
* Docker
* GitHub Actions
* Git and GitHub

---

## Project Structure

```text
mis-cloudops-dashboard/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── services_router.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── service_service.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── service_repo.py
│   │
│   └── schemas/
│       ├── __init__.py
│       └── service_schema.py
│
├── tests/
│   ├── test_health.py
│   └── test_services.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
└── .gitignore
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Checks if the API is running.

---

### Create a Service

```http
POST /services
```

Example request:

```json
{
  "name": "Email Server",
  "url": "https://mail.example.com",
  "owner": "MIS Team"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Email Server",
  "url": "https://mail.example.com",
  "owner": "MIS Team",
  "status": "unknown"
}
```

---

### List All Services

```http
GET /services
```

Example response:

```json
{
  "services": [
    {
      "id": 1,
      "name": "Email Server",
      "url": "https://mail.example.com",
      "owner": "MIS Team",
      "status": "unknown",
      "created_at": "2026-06-11T12:00:00",
      "updated_at": "2026-06-11T12:00:00"
    }
  ]
}
```

---

### Get a Service by ID

```http
GET /services/{service_id}
```

Example:

```http
GET /services/1
```

If the service exists, it returns that service.

If the service does not exist, it returns:

```json
{
  "detail": "Service not found"
}
```

---

### Update Service Status

```http
PATCH /services/{service_id}/status
```

Example request:

```json
{
  "status": "online"
}
```

Allowed status values:

```text
unknown
online
offline
degraded
```

If an invalid status is sent, the API returns a validation error.

---

### Delete a Service by ID

```http
DELETE /services/{service_id}
```

Example:

```http
DELETE /services/1
```

If the service exists, it is removed and returned in the response.

If the service does not exist, it returns:

```json
{
  "detail": "Service not found"
}
```

---

## Database

This project uses SQLite for local data storage.

The database is initialized when the FastAPI app starts. Services are stored in a local `services.db` file, which is ignored by Git so local data is not pushed to GitHub.

The services table stores:

```text
id
name
url
owner
status
created_at
updated_at
```

The `created_at` field stores when a service was first created.

The `updated_at` field stores when a service was last updated.
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/beabgirma/mis-cloudops-dashboard.git
cd mis-cloudops-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

### 6. Open the API docs

Go to:

```text
http://127.0.0.1:8000/docs
```

FastAPI will show an interactive documentation page where you can test the endpoints.

---

## Run with Docker

This project can also be run inside a Docker container.

### Build the Docker image

```bash
docker build -t mis-cloudops-dashboard .
```

### Run the container

```bash
docker run -p 8000:8000 mis-cloudops-dashboard
```

### Open the API docs

Once the container is running, open:

```text
http://127.0.0.1:8000/docs
```

### Stop the container

Press:

```bash
CTRL + C
```

The API runs on port `8000` inside the container and is accessible from the browser at `localhost:8000`.

---

## How to Run Tests

Run:

```bash
pytest
```

The project includes tests for:

* Health check endpoint
* Creating services
* Listing services
* Getting a service by ID
* Updating service status
* Invalid status validation
* Deleting services
* 404 error handling

---

## GitHub Actions

This project uses GitHub Actions to automatically run tests when changes are pushed or when a pull request is opened.

The workflow helps make sure new changes do not break the existing API.

---

## What I Learned

While building this project, I practiced:

* Creating FastAPI routes
* Using Pydantic schemas for validation
* Structuring a backend project with routers, services, and repositories
* Using SQLite for persistent local storage
* Writing automated tests with Pytest
* Handling API errors with proper status codes
* Using Git branches and pull requests
* Running automated tests with GitHub Actions
* Building and running the API with Docker
* Building a backend project with a more professional workflow

---

## Current Status

Completed features:

* Health check endpoint
* Service creation
* Service listing
* Get service by ID
* Update service status
* Delete service by ID
* Status validation
* SQLite database storage
* Created and updated timestamps
* Docker support
* Automated tests
* GitHub Actions CI


---

## Future Improvements

Possible next steps:

* Add service categories or tags
* Add timestamps for created and updated services
* Add authentication
* Add PostgreSQL support for production
* Deploy the API online
* Add a frontend dashboard
