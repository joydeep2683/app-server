# app-server

FastAPI application with SQLAlchemy for managing educators, students, and call requests.

## Setup Instructions

### 1. Create and activate virtual environment
```bash
pip install virtualenv
virtualenv .venv -p python3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and update the database configuration:
```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL database credentials:
```
PG_DB_NAME=your_database_name
PG_DB_USER=your_database_user
PG_DB_PASSWORD=your_database_password
PG_DB_HOST=localhost
PG_DB_PORT=5432
```

### 4. Initialize the database (optional)
If you prefer to create database tables manually before starting the server:
```bash
python init_db.py
```

Note: Tables will also be automatically created when the FastAPI server starts.

### 5. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Area
- `GET /api/v1/area` - List all areas
- `POST /api/v1/area` - Create an area
- `POST /api/v1/area/bulk` - Bulk create areas
- `GET /api/v1/area/{id}` - Get area by ID
- `PUT /api/v1/area/{id}` - Update area
- `DELETE /api/v1/area/{id}` - Delete area

### Degree
- `GET /api/v1/degree` - List all degrees
- `POST /api/v1/degree` - Create a degree
- `POST /api/v1/degree/bulk` - Bulk create degrees
- `GET /api/v1/degree/{id}` - Get degree by ID
- `PUT /api/v1/degree/{id}` - Update degree
- `DELETE /api/v1/degree/{id}` - Delete degree

### Students
- `GET /api/v1/students` - List all students
- `POST /api/v1/students` - Create a student
- `GET /api/v1/students/{id}` - Get student by ID
- `PUT /api/v1/students/{id}` - Update student
- `PATCH /api/v1/students/{id}` - Partial update student
- `DELETE /api/v1/students/{id}` - Delete student

### Educators
- `GET /api/v1/educators` - List all educators
- `POST /api/v1/educators` - Create an educator
- `GET /api/v1/educators/{id}` - Get educator by ID
- `PUT /api/v1/educators/{id}` - Update educator
- `PATCH /api/v1/educators/{id}` - Partial update educator
- `DELETE /api/v1/educators/{id}` - Delete educator

### Call Requests
- `GET /api/v1/calls` - List all call requests
- `POST /api/v1/calls` - Create a call request
- `GET /api/v1/calls/{id}` - Get call request by ID
- `PUT /api/v1/calls/{id}` - Update call request
- `PATCH /api/v1/calls/{id}` - Partial update call request
- `DELETE /api/v1/calls/{id}` - Delete call request

