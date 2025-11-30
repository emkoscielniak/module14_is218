# FastAPI Calculator with User Management & CRUD Operations

A comprehensive FastAPI application featuring user authentication, calculation CRUD operations, and secure password management. Built with SQLAlchemy ORM, Pydantic validation, and deployed via Docker Hub with complete CI/CD pipeline.

## 🎯 Features

- **User Management**: Complete user registration and login system with JWT authentication
- **Calculation CRUD**: Full BREAD operations (Browse, Read, Edit, Add, Delete) for calculations
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Input Validation**: Comprehensive Pydantic validation with custom password requirements
- **Database Integration**: SQLAlchemy ORM with PostgreSQL support
- **Comprehensive Testing**: Unit and integration tests with pytest
- **CI/CD Pipeline**: Automated testing, security scanning, and Docker Hub deployment
- **OpenAPI Documentation**: Interactive API documentation with Swagger UI

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull and run the latest image from Docker Hub
docker run -p 8000:8000 emkoscielniak/module12_is218:latest
```

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd module12_is218

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL required)
export DATABASE_URL="postgresql://user:password@localhost:5432/your_db"

# Run the application
python main.py
```

The application will be available at `http://localhost:8000`

## 📋 API Endpoints

### User Management
- `POST /users/register` - Register a new user with UserCreate schema
- `POST /users/login` - Login with username/password, returns JWT token
- `GET /users/me` - Get current authenticated user information

### Calculation CRUD (BREAD)
- `GET /calculations` - Browse all calculations with pagination (skip, limit)
- `GET /calculations/{id}` - Read a specific calculation by ID
- `POST /calculations` - Add a new calculation using CalculationCreate schema
- `PUT /calculations/{id}` - Edit/update an existing calculation
- `DELETE /calculations/{id}` - Delete a calculation by ID

### Legacy Endpoints
- `GET /` - Homepage with calculator interface
- `POST /register` - Legacy user registration (redirects to /users/register)
- `POST /login` - Legacy OAuth2 form login
- `POST /login/json` - JSON login endpoint
- `GET /health` - Health check endpoint
- Calculator endpoints: `/add`, `/subtract`, `/multiply`, `/divide`

## 🧪 Running Tests Locally

### Prerequisites
- PostgreSQL database running locally
- Virtual environment activated with dependencies installed

### Test Commands

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests  
pytest tests/integration/ -v

# Run specific test file
pytest tests/integration/test_user_registration_login.py -v
pytest tests/integration/test_calculation_endpoints.py -v

# Run tests with detailed output
pytest tests/ -v --tb=short
```

### Test Categories

- **Unit Tests**: Test individual components (password hashing, calculation factory, schema validation)
- **Integration Tests**: Test complete API workflows with database integration
  - User registration and login flows
  - Calculation CRUD operations
  - Input validation and error handling
  - Database persistence and data integrity

## 🔍 Manual Testing via OpenAPI

Access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs  
- **ReDoc**: http://localhost:8000/redoc

### Testing User Endpoints
1. **Register a User**: Use `/users/register` with valid user data
2. **Login**: Use `/users/login` to get an authentication token  
3. **Access Protected Routes**: Use the "Authorize" button in Swagger UI with your token

### Testing Calculation Endpoints  
1. **Create Calculations**: Use `/calculations` POST with different operation types
2. **Browse Calculations**: Use `/calculations` GET with pagination parameters
3. **Update Calculations**: Use `/calculations/{id}` PUT to modify existing calculations
4. **Validate Input**: Test invalid data (division by zero, invalid types) to verify error handling

## 🐳 Docker Hub Repository

**Docker Hub Link**: [https://hub.docker.com/r/emkoscielniak/module12_is218](https://hub.docker.com/r/emkoscielniak/module12_is218)

The Docker image is automatically built and pushed via GitHub Actions on every successful test run on the main branch.
- **E2E Tests**: End-to-end browser testing with Playwright

## 🐳 Docker Hub Repository

The application is automatically built and deployed to Docker Hub:

**Repository**: [emkoscielniak/module10_is601](https://hub.docker.com/r/emkoscielniak/module10_is601)

Available tags:
- `latest` - Latest stable version
- `<git-sha>` - Specific commit versions

### Using Different Versions

```bash
# Latest version
docker pull emkoscielniak/module10_is601:latest

# Specific version
docker pull emkoscielniak/module10_is601:<git-sha>
```

## 🛡️ Security Features

- **Password Hashing**: bcrypt with salt for secure password storage
- **JWT Tokens**: Secure authentication with configurable expiration
- **Input Validation**: Pydantic schemas prevent injection attacks
- **Security Scanning**: Trivy vulnerability scanning in CI/CD
- **Database**: PostgreSQL with proper ORM usage preventing SQL injection

## 🏗️ Architecture

- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with OAuth2 password bearer
- **Validation**: Pydantic v2 with custom validators
- **Testing**: pytest with fixtures and dependency injection
- **Deployment**: Docker with multi-stage builds

## 📦 Project Setup

### 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
