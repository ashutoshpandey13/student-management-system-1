# Student Database Management API

A simple REST API for managing student records with CRUD operations, built with Flask. Uses in-memory storage (no database).

## Vulnerabilities

This project intentionally uses **cryptography version 46.0.5** which contains the following vulnerabilities:
- **CVE-2026-39892** (Medium severity, CVSS 5.3)
- **CVE-2026-34073** (Low severity, CVSS 3.7)

## Features

- Create, Read, Update, and Delete student records
- In-memory storage (runtime only, no database)
- Data encryption/decryption demonstration using cryptography library
- RESTful API endpoints
- Docker support
- Data persists only while container is running

## API Endpoints

### Health Check
- **GET** `/health` - Check API status

### Student Operations
- **POST** `/api/students` - Create a new student
- **GET** `/api/students` - Get all students
- **GET** `/api/students/<id>` - Get a specific student
- **PUT** `/api/students/<id>` - Update a student
- **DELETE** `/api/students/<id>` - Delete a student

### Encryption Demo
- **POST** `/api/encrypt` - Encrypt text data
- **POST** `/api/decrypt` - Decrypt text data

### Utility
- **DELETE** `/api/students/clear` - Clear all students from memory

## Request Examples

### Create Student
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 20,
    "course": "Computer Science"
  }'
```

### Get All Students
```bash
curl http://localhost:5000/api/students
```

### Get Student by ID
```bash
curl http://localhost:5000/api/students/1
```

### Update Student
```bash
curl -X PUT http://localhost:5000/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "age": 21
  }'
```

### Delete Student
```bash
curl -X DELETE http://localhost:5000/api/students/1
```

## Building and Running with Docker

### Build the Docker Image
```bash
cd student-api
docker build -t student-api:vulnerable .
```

### Run the Container
```bash
docker run -p 5000:5000 student-api:vulnerable
```

### Scan for Vulnerabilities
You can scan the built image using various security scanning tools:

```bash
# Using Docker Scout
docker scout cves student-api:vulnerable

# Using Trivy
trivy image student-api:vulnerable

# Using Snyk
snyk container test student-api:vulnerable
```

## Running Locally (without Docker)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

**Note:** All student data is stored in memory only. When you stop the application, all data will be lost.

## Project Structure
```
student-api/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies (includes vulnerable cryptography 46.0.5)
├── Dockerfile         # Docker configuration
└── README.md          # This file
```

## Security Note

⚠️ **WARNING**: This project intentionally uses vulnerable dependencies for demonstration purposes. Do NOT use this in production environments. Always use the latest secure versions of dependencies in production applications.

To fix the vulnerabilities, update cryptography to version 46.0.7 or later:
```bash
pip install cryptography>=46.0.7