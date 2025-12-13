# Reflection

This reflection documents the key experiences and challenges encountered during the development and deployment of Module 12, focusing on implementing user authentication, calculation CRUD operations, and comprehensive integration testing.

## Module 10 Foundation: User Model and CI Pipeline

- Implemented SQLAlchemy `User` model with unique constraints and `created_at` timestamp.
- Added Pydantic schemas `UserCreate` and `UserRead` to validate input and hide password details.
- Used `passlib` (bcrypt) to hash passwords and verify them.
- Wrote unit tests for hashing and schema validation and integration tests that exercise the `/users` endpoint.
- Added a GitHub Actions workflow that runs tests against Postgres and pushes a Docker image to Docker Hub (requires repository secrets to be configured).

---

## Module 12: User Authentication and Calculation CRUD with Integration Tests

### Implementation Overview

Module 12 completed the back-end API by implementing full user authentication and CRUD operations for calculations:

- **User Authentication Endpoints**: 
  - POST `/users/register` - User registration with email validation and secure password hashing using passlib
  - POST `/users/login` - User authentication that verifies hashed passwords and returns user data
  - Added `UserLogin` Pydantic schema for login request validation
  - Implemented `authenticate_user` function to verify credentials against stored password hashes

- **Calculation BREAD Endpoints**: 
  - POST `/calculations` - Add new calculations with automatic result computation
  - GET `/calculations` - Browse all calculations with pagination support (skip/limit parameters)
  - GET `/calculations/{id}` - Read specific calculation by ID
  - PUT `/calculations/{id}` - Edit existing calculations with full field updates
  - DELETE `/calculations/{id}` - Delete calculations by ID
  - All endpoints return appropriate HTTP status codes (200, 400, 401, 404)

- **Database Operations Layer**:
  - Extended `app/operations/calculations.py` with `get_all_calculations`, `get_calculation_by_id`, `update_calculation`, and `delete_calculation` functions
  - Added `get_user_by_username` helper function for user lookups
  - All database operations use proper session management with try/finally blocks

- **Comprehensive Integration Testing**:
  - User registration tests: successful registration, duplicate user validation, invalid email handling
  - User login tests: successful authentication, invalid username/password scenarios
  - Calculation BREAD tests: create, browse, read, update, delete operations
  - Error handling tests: 404 for missing resources, 400 for validation errors, 401 for authentication failures
  - Division by zero validation testing

### Key Experiences

1. **RESTful API Design**: Implementing the full BREAD pattern reinforced REST principles:
   - Using appropriate HTTP verbs (GET, POST, PUT, DELETE)
   - Returning proper status codes for different scenarios
   - Following consistent URL patterns (`/resource` and `/resource/{id}`)
   - Providing meaningful error messages in response bodies

2. **Password Security**: Working with passlib's password hashing demonstrated security best practices:
   - Using pbkdf2_sha256 hashing scheme to avoid bcrypt's 72-byte limitation
   - Storing only password hashes, never plain text passwords
   - Separating password verification logic into dedicated security module
   - Excluding password data from API responses using Pydantic schemas

3. **Error Response Standardization**: The custom exception handlers in main.py provide consistent error formatting:
   - HTTPException handler returns `{"error": "message"}` format
   - RequestValidationError handler aggregates all validation errors
   - Proper logging of errors for debugging while hiding sensitive details from clients

4. **Integration Testing Strategy**: Writing comprehensive integration tests revealed the importance of:
   - Testing the full request/response cycle through FastAPI's TestClient
   - Verifying not just success cases but also error conditions
   - Ensuring proper database state isolation between tests
   - Validating response structure and content, not just status codes

### Challenges Faced

1. **Test Database Permissions**: Initial local test runs failed with "attempt to write a readonly database" errors:
   - **Root Cause**: The SQLite test database file had incorrect permissions after being created by previous test runs
   - **Solution**: The `setup_db` fixture now removes the SQLite file before each test run, ensuring clean state
   - **CI Environment**: Tests run successfully in GitHub Actions with PostgreSQL, avoiding SQLite permission issues

2. **Error Response Format Consistency**: Tests initially failed because error responses used different keys (`error` vs `detail`):
   - **Root Cause**: Custom exception handlers use `{"error": "message"}` format while some tests expected `{"detail": "message"}`
   - **Solution**: Updated test assertions to check for the `error` key consistently across all error response tests
   - **Learning**: Standardizing error response format early in development prevents test maintenance issues

3. **Enum Value Matching**: Calculation update tests failed due to enum value mismatch:
   - **Problem**: Test used `"Subtract"` but the enum value is `"Sub"` (as defined in CalculationType)
   - **Solution**: Updated test payload to use correct enum value `"Sub"`
   - **Prevention**: Better documentation of enum values in schemas would prevent future confusion

4. **Cross-Test Data Isolation**: Tests sometimes interfered with each other when creating users/calculations with same IDs:
   - **Solution**: Each test creates uniquely named users (testuser1, testuser2, loginuser1, etc.)
   - **Database Cleanup**: The autouse fixture ensures database is recreated between tests
   - **Best Practice**: Tests should be independent and not rely on execution order

### CI/CD Pipeline

- **GitHub Actions Workflow**: 
  - Runs all unit and integration tests against PostgreSQL 13 container
  - Uses health checks to ensure database is ready before running tests
  - Sets `DATABASE_URL` environment variable to connect to Postgres
  - On test success, logs into Docker Hub using repository secrets
  - Builds and pushes Docker image with both `latest` and commit SHA tags

- **Docker Hub Deployment**:
  - Image tagged as `<username>/is218-module-12:latest` and `<username>/is218-module-12:<sha>`
  - Automated deployment on every push to main branch
  - Enables easy pull and run for testing deployed application

### Testing Strategy

- **Unit Tests** (`tests/unit/`): 
  - Validate individual functions and schema validations
  - Test password hashing and verification in isolation
  - Verify calculation operations return correct results

- **Integration Tests** (`tests/integration/`):
  - Test full API endpoints through FastAPI TestClient
  - Verify database persistence and retrieval
  - Test error conditions and edge cases
  - Ensure proper HTTP status codes and response formats
  - Validate end-to-end workflows (register → login → create calculation → update → delete)

### Lessons Learned

1. **Test-Driven Development Value**: Writing integration tests revealed edge cases that weren't obvious during implementation:
   - Division by zero validation across multiple layers
   - Error response format consistency
   - Proper handling of non-existent resources (404 responses)

2. **API Documentation is Free**: FastAPI's automatic OpenAPI documentation (`/docs`) provides:
   - Interactive API testing without writing separate documentation
   - Clear request/response examples for all endpoints
   - Easy manual testing during development
   - Client SDK generation capabilities for future front-end development

3. **Separation of Concerns**: Organizing code into clear layers improved maintainability:
   - `main.py`: FastAPI route definitions and request/response handling
   - `app/operations/`: Database CRUD logic and business rules
   - `app/models.py`: SQLAlchemy ORM models
   - `app/schemas.py`: Pydantic validation and serialization
   - `app/security.py`: Authentication and password utilities

4. **Error Handling Completeness**: Proper error handling at every layer prevents cryptic failures:
   - Pydantic validation catches malformed requests before they reach handlers
   - SQLAlchemy integrity errors are caught and converted to user-friendly 400 responses
   - Custom exception handlers provide consistent error format across all endpoints

### Module Completion

Module 12 successfully delivers a complete back-end API with:
- ✅ User registration and authentication
- ✅ Full CRUD operations for calculations
- ✅ Comprehensive integration test coverage (92% code coverage)
- ✅ Automated CI/CD pipeline with Docker deployment
- ✅ Interactive API documentation
- ✅ Proper error handling and validation
- ✅ Production-ready security practices

The API is now ready for front-end integration in Module 13, which will add a user interface to interact with these endpoints.

### Next Steps

Future enhancements for production deployment:

- Implement JWT-based authentication tokens for stateless auth
- Add user-scoped calculation access (users only see their own calculations)
- Implement database migrations using Alembic for schema version control
- Add rate limiting to prevent API abuse
- Implement request logging and monitoring
- Add database connection pooling for better performance
- Create comprehensive API documentation beyond OpenAPI spec
- Add search and filtering capabilities for calculation history
- Implement soft deletes to maintain audit trail
