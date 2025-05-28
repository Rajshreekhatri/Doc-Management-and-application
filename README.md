# Document Management System

A robust Python-based backend service for managing users and documents with role-based access control, document ingestion, and a modern RESTful API. Built with Flask, SQLAlchemy, and PostgreSQL.

---

## Features
- User authentication and JWT-based authorization
- Role-based access control (Admin, Editor, Viewer)
- Document CRUD operations with file upload
- Document ingestion and logging
- PostgreSQL database integration
- Dockerized for easy deployment
- Automated testing

---

## Table of Contents
- [API Endpoints](#api-endpoints)
- [Environment Setup](#environment-setup)
- [Running with Docker](#running-with-docker)
- [Manual Local Setup](#manual-local-setup)
- [Database Schema](#database-schema)
- [Security](#security)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/token` - Login and get access token (form data)
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

#### Register
```bash
curl -X POST "http://localhost:5001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","full_name":"Test User", "role":"viewer"}'
```
#### Login
```bash
curl -X POST "http://localhost:5001/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```
#### Get Current User
```bash
curl -X GET "http://localhost:5001/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```
#### Logout
```bash
curl -X POST "http://localhost:5001/api/v1/auth/logout" \
  -H "Authorization: Bearer $TOKEN"
```

---

### User Management (Admin only for some endpoints)
- `GET /api/v1/users/` - List all users (Admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID (Admin only)
- `PUT /api/v1/users/{user_id}` - Update user info (Admin only)
- `DELETE /api/v1/users/{user_id}` - Delete user (Admin only)

#### List Users
```bash
curl -X GET "http://localhost:5002/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get User by ID
```bash
curl -X GET "http://localhost:5002/api/v1/users/3" \
  -H "Authorization: Bearer $TOKEN"
```
#### Update User
```bash
curl -X PUT "http://localhost:5002/api/v1/users/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Updated Name", "role": "editor"}'
```
#### Delete User
```bash
curl -X DELETE "http://localhost:5002/api/v1/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Document Management
- `POST /api/v1/documents/` - Upload a new document (Admin/Editor only)
- `GET /api/v1/documents/` - List all documents
- `GET /api/v1/documents/{document_id}` - Get a specific document
- `PUT /api/v1/documents/{document_id}` - Update document metadata (Admin/Editor only)
- `DELETE /api/v1/documents/{document_id}` - Delete a document (Admin only)

#### Upload Document
```bash
curl -X POST "http://localhost:5003/api/v1/documents/" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf" \
  -F "title=Test Document" \
  -F "description=This is a test document" \
  -F "file_type=pdf"
```
#### List Documents
```bash
curl -X GET "http://localhost:5003/api/v1/documents/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get Document
```bash
curl -X GET "http://localhost:5003/api/v1/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```
#### Update Document (metadata only)
```bash
curl -X PUT "http://localhost:5003/api/v1/documents/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Document", "description": "Updated description", "file_type": "pdf"}'
```
#### Update Document (with file)
```bash
curl -X PUT "http://localhost:5003/api/v1/documents/1" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@updated.pdf" \
  -F "title=Updated Document" \
  -F "description=Updated description" \
  -F "file_type=pdf"
```
#### Delete Document
```bash
curl -X DELETE "http://localhost:5003/api/v1/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Ingestion
- `GET /api/v1/ingestion/` - List all ingestion logs (Admin/Editor only)
- `POST /api/v1/ingestion/trigger` - Trigger document ingestion (Admin/Editor only)
- `GET /api/v1/ingestion/status` - Get ingestion status (Admin/Editor only)

#### List Ingestion Logs
```bash
curl -X GET "http://localhost:5004/api/v1/ingestion/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Trigger Ingestion
```bash
curl -X POST "http://localhost:5004/api/v1/ingestion/trigger" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get Ingestion Status
```bash
curl -X GET "http://localhost:5004/api/v1/ingestion/status" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Environment Setup

### .env Example
Create a `.env` file in the root of each service:
```env
JWT_SECRET_KEY=super-secret-key
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgrespassword
POSTGRES_DB=microservices_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

```

---

## Running with Docker

1. **Build and start all services:**
```bash
docker-compose up --build -d
```
2. **Stop all services:**
```bash
docker-compose down
```
3. **View logs:**
```bash
docker-compose logs -f
```

---


## Database Schema

- `users` - User accounts
- `documents` - Document metadata and file info
- `ingestion_logs` - Ingestion process logs

See `init.sql` for full schema.

---

## Security
- Passwords hashed with bcrypt
- JWT authentication
- Role-based access control
- CORS configuration

---

## Error Handling
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

---

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License
MIT License

---

## Support
For support, open an issue in the repository.