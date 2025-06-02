# Medication Management API

A FastAPI-based REST API for managing patient medication requests in a healthcare setting.

## Features

- **Patient Management**: Store patient demographics
- **Clinician Management**: Track healthcare providers
- **Medication Catalog**: Maintain medication database with codes and specifications
- **Medication Requests**: Create, read, and update medication prescriptions
- **Filtering**: Search requests by status and date ranges
- **Validation**: Pydantic models for request/response validation
- **Testing**: Comprehensive test suite with pytest
- **Type Safety**: MyPy static type checking
- **Containerization**: Docker support

## Quick Start

### Local Development

1. **Setup environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database setup**:
   ```bash
   # For PostgreSQL
   export DATABASE_URL="postgresql://user:password@localhost/medication_db"
   
   # Or use SQLite for development (default)
   # No setup needed - SQLite file will be created automatically
   ```

3. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```
### Using Docker

1. **Clone and build**:
   ```bash
   git clone https://github.com/pradeepkumar2230/task_code
   cd task_code
   docker-compose up --build
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Medication Requests

- `POST /patients/{patient_id}/medication-requests` - Create new medication request
- `GET /patients/{patient_id}/medication-requests` - Get requests with optional filtering
- `PATCH /patients/{patient_id}/medication-requests/{request_id}` - Update request

### Query Parameters for GET

- `status`: Filter by status (active, on-hold, cancelled, completed)
- `prescribed_from`: Filter from date (YYYY-MM-DD)
- `prescribed_to`: Filter to date (YYYY-MM-DD)

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest test_main.py -v
```

## Type Checking

```bash
mypy .
```

## Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Assumptions and Design Decisions

### Database Design
- Uses integer primary keys for all entities
- Foreign key relationships between MedicationRequest and other entities
- Enum types for constrained fields (sex, form, status)

### API Design
- RESTful design with resource-based URLs
- Patient ID in URL path for clear resource ownership
- PATCH endpoint only allows updating specific fields (end_date, frequency, status)
- GET endpoint includes related entity data (clinician name, medication name)

### Validation and Testing Strategy
- Required fields enforced at database and API level
- Date validation using Pydantic
- Enum validation for constrained choices
- Unit tests for API endpoints
- Test database isolation using SQLite
- Fixture-based test data setup
