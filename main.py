# main.py

from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, field_validator  # Use @validator for Pydantic 1.x
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from app.operations import add, subtract, multiply, divide  # Ensure correct import path
from app.database import get_db
from app.models.user import User
from app.models.calculation import Calculation
from app.schemas.base import UserCreate, UserRead
from app.schemas.user import UserResponse, Token, UserLogin
from app.schemas.calculation import CalculationCreate, CalculationRead, CalculationUpdate
from app.auth.dependencies import get_current_user, get_current_active_user
from typing import List
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# Pydantic model for request data
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')  # Correct decorator for Pydantic 1.x
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value

# Pydantic model for successful response
class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")

# Pydantic model for error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")

# Custom Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extracting error messages
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )

@app.get("/")
async def read_root(request: Request):
    """
    Serve the index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    """
    Serve the registration page.
    """
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    """
    Serve the login page.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    """
    Add two numbers.
    """
    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    """
    Subtract two numbers.
    """
    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Subtract Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers.
    """
    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Multiply Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    """
    Divide two numbers.
    """
    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e:
        logger.error(f"Divide Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Divide Operation Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# User Authentication and Registration Routes
@app.post("/users/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user using UserCreate schema.
    """
    try:
        # Truncate password to avoid bcrypt 72-byte limit
        user_dict = user_data.model_dump()
        if 'password' in user_dict:
            password_bytes = user_dict['password'].encode('utf-8')[:72]
            user_dict['password'] = password_bytes.decode('utf-8', errors='ignore')
        
        user = User.register(db, user_dict)
        db.commit()
        db.refresh(user)
        return UserRead.model_validate(user)
    except ValueError as e:
        logger.error(f"User registration error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected registration error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/users/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token verifying hashed passwords.
    """
    try:
        token_data = User.authenticate(db, user_credentials.username, user_credentials.password)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Legacy endpoints for backward compatibility
@app.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user_legacy(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user (legacy endpoint).
    """
    return await register_user(user_data, db)

@app.post("/login", response_model=Token)
async def login_user_legacy(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token (legacy endpoint).
    """
    try:
        token_data = User.authenticate(db, form_data.username, form_data.password)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/login/json", response_model=Token)
async def login_user_json(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with JSON payload and return access token.
    """
    try:
        token_data = User.authenticate(db, user_credentials.username, user_credentials.password)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"JSON Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Get current user information.
    """
    return current_user

# Calculation BREAD endpoints
@app.get("/calculations", response_model=List[CalculationRead])
async def browse_calculations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Browse all calculations belonging to the logged-in user with pagination.
    """
    try:
        calculations = db.query(Calculation).filter(
            Calculation.user_id == current_user.id
        ).offset(skip).limit(limit).all()
        return [CalculationRead.model_validate(calc) for calc in calculations]
    except Exception as e:
        logger.error(f"Browse calculations error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/calculations/{id}", response_model=CalculationRead)
async def read_calculation(
    id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Read a specific calculation by ID (user-specific).
    """
    try:
        calculation = db.query(Calculation).filter(
            Calculation.id == id,
            Calculation.user_id == current_user.id
        ).first()
        if not calculation:
            raise HTTPException(status_code=404, detail="Calculation not found")
        return CalculationRead.model_validate(calculation)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Read calculation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/calculations", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
async def add_calculation(
    calculation_data: CalculationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Add a new calculation for the logged-in user using CalculationCreate schema.
    """
    try:
        # Create the calculation instance
        calculation = Calculation(
            a=calculation_data.a,
            b=calculation_data.b,
            type=calculation_data.type,
            user_id=current_user.id
        )
        
        # Compute the result
        calculation.result = calculation.compute()
        
        # Save to database
        db.add(calculation)
        db.commit()
        db.refresh(calculation)
        
        return CalculationRead.model_validate(calculation)
    except ValueError as e:
        logger.error(f"Add calculation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected add calculation error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/calculations/{id}", response_model=CalculationRead)
async def edit_calculation(
    id: int,
    calculation_update: CalculationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Edit/update an existing calculation (user-specific).
    """
    try:
        calculation = db.query(Calculation).filter(
            Calculation.id == id,
            Calculation.user_id == current_user.id
        ).first()
        if not calculation:
            raise HTTPException(status_code=404, detail="Calculation not found")
        
        # Update fields that are provided
        update_data = calculation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(calculation, field, value)
        
        # Recalculate result if a, b, or type was updated
        if any(key in update_data for key in ['a', 'b', 'type']):
            calculation.result = calculation.compute()
        
        db.commit()
        db.refresh(calculation)
        
        return CalculationRead.model_validate(calculation)
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Edit calculation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected edit calculation error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.patch("/calculations/{id}", response_model=CalculationRead)
async def patch_calculation(
    id: int,
    calculation_update: CalculationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Partially update an existing calculation (user-specific).
    """
    try:
        calculation = db.query(Calculation).filter(
            Calculation.id == id,
            Calculation.user_id == current_user.id
        ).first()
        if not calculation:
            raise HTTPException(status_code=404, detail="Calculation not found")
        
        # Update fields that are provided
        update_data = calculation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(calculation, field, value)
        
        # Recalculate result if a, b, or type was updated
        if any(key in update_data for key in ['a', 'b', 'type']):
            calculation.result = calculation.compute()
        
        db.commit()
        db.refresh(calculation)
        
        return CalculationRead.model_validate(calculation)
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Patch calculation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected patch calculation error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/calculations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calculation(
    id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a calculation by ID (user-specific).
    """
    try:
        calculation = db.query(Calculation).filter(
            Calculation.id == id,
            Calculation.user_id == current_user.id
        ).first()
        if not calculation:
            raise HTTPException(status_code=404, detail="Calculation not found")
        
        db.delete(calculation)
        db.commit()
        
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete calculation error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and Docker health checks.
    """
    return {"status": "healthy", "timestamp": "2025-11-30"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
