# tests/e2e/test_e2e.py

import pytest  # Import the pytest framework for writing and running tests
import time

# The following decorators and functions define E2E tests for the FastAPI calculator application.

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage displays "Hello World".

    This test verifies that when a user navigates to the homepage of the application,
    the main header (`<h1>`) correctly displays the text "Hello World". This ensures
    that the server is running and serving the correct template.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Use an assertion to check that the text within the first <h1> tag is exactly "Hello World".
    # If the text does not match, the test will fail.
    assert page.inner_text('h1') == 'Hello World'

@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """
    Test the addition functionality of the calculator.

    This test simulates a user performing an addition operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Add" button, and verifies
    that the result displayed is correct.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '5'.
    page.fill('#b', '5')
    
    # Click the button that has the exact text "Add". This triggers the addition operation.
    page.click('button:text("Add")')
    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly "Result: 15".
    # This verifies that the addition operation was performed correctly and the result is displayed as expected.
    assert page.inner_text('#result') == 'Result: 15'

# JWT Authentication E2E Tests

@pytest.mark.e2e
def test_register_with_valid_data(page, fastapi_server):
    """
    Positive test: Register with valid data (email format, password length).
    Should confirm success message.
    """
    # Navigate to the registration page
    page.goto('http://localhost:8000/register')
    
    # Fill in valid registration data
    page.fill('#firstName', 'John')
    page.fill('#lastName', 'Doe')
    page.fill('#username', 'johndoe123')
    page.fill('#email', 'john.doe@example.com')
    page.fill('#password', 'SecurePass123')
    page.fill('#confirmPassword', 'SecurePass123')
    
    # Submit the form
    page.click('button[type="submit"]')
    
    # Wait for the success message to appear
    page.wait_for_selector('#successMessage', state='visible', timeout=10000)
    
    # Verify success message is displayed
    assert page.is_visible('#successMessage')
    assert 'Registration successful' in page.inner_text('#successMessage')

@pytest.mark.e2e
def test_login_with_correct_credentials(page, fastapi_server):
    """
    Positive test: Login with correct credentials.
    Should confirm success or token stored.
    """
    # First, register a user
    page.goto('http://localhost:8000/register')
    page.fill('#firstName', 'Jane')
    page.fill('#lastName', 'Smith')
    page.fill('#username', 'janesmith')
    page.fill('#email', 'jane.smith@example.com')
    page.fill('#password', 'Password123')
    page.fill('#confirmPassword', 'Password123')
    page.click('button[type="submit"]')
    
    # Wait for registration to complete
    page.wait_for_selector('#successMessage', state='visible', timeout=10000)
    
    # Now navigate to login page
    page.goto('http://localhost:8000/login')
    
    # Fill in correct login credentials
    page.fill('#username', 'janesmith')
    page.fill('#password', 'Password123')
    
    # Submit login form
    page.click('button[type="submit"]')
    
    # Wait for success message or token display
    page.wait_for_selector('#tokenInfo', state='visible', timeout=10000)
    
    # Verify login was successful
    assert page.is_visible('#tokenInfo')
    assert 'Login Successful' in page.inner_text('#tokenInfo')

@pytest.mark.e2e
def test_register_with_short_password(page, fastapi_server):
    """
    Negative test: Register with short password.
    Should show front-end error or 400 from server, verify UI shows error.
    """
    # Navigate to the registration page
    page.goto('http://localhost:8000/register')
    
    # Fill in registration data with short password
    page.fill('#firstName', 'Test')
    page.fill('#lastName', 'User')
    page.fill('#username', 'testuser')
    page.fill('#email', 'test@example.com')
    page.fill('#password', '123')  # Short password
    page.fill('#confirmPassword', '123')
    
    # Submit the form
    page.click('button[type="submit"]')
    
    # Wait for error message to appear
    page.wait_for_selector('#passwordError', state='visible', timeout=5000)
    
    # Verify error message is displayed
    assert page.is_visible('#passwordError')
    assert 'at least 6 characters' in page.inner_text('#passwordError')

@pytest.mark.e2e  
def test_register_with_invalid_email(page, fastapi_server):
    """
    Negative test: Register with invalid email format.
    Should show front-end validation error.
    """
    # Navigate to the registration page
    page.goto('http://localhost:8000/register')
    
    # Fill in registration data with invalid email
    page.fill('#firstName', 'Test')
    page.fill('#lastName', 'User')
    page.fill('#username', 'testuser2')
    page.fill('#email', 'invalid-email')  # Invalid email format
    page.fill('#password', 'Password123')
    page.fill('#confirmPassword', 'Password123')
    
    # Submit the form
    page.click('button[type="submit"]')
    
    # Wait for error message to appear
    page.wait_for_selector('#emailError', state='visible', timeout=5000)
    
    # Verify error message is displayed
    assert page.is_visible('#emailError')
    assert 'valid email address' in page.inner_text('#emailError')

@pytest.mark.e2e
def test_register_with_mismatched_passwords(page, fastapi_server):
    """
    Negative test: Register with mismatched passwords.
    Should show front-end validation error.
    """
    # Navigate to the registration page
    page.goto('http://localhost:8000/register')
    
    # Fill in registration data with mismatched passwords
    page.fill('#firstName', 'Test')
    page.fill('#lastName', 'User')
    page.fill('#username', 'testuser3')
    page.fill('#email', 'test3@example.com')
    page.fill('#password', 'Password123')
    page.fill('#confirmPassword', 'DifferentPassword123')  # Mismatched password
    
    # Submit the form
    page.click('button[type="submit"]')
    
    # Wait for error message to appear
    page.wait_for_selector('#confirmPasswordError', state='visible', timeout=5000)
    
    # Verify error message is displayed
    assert page.is_visible('#confirmPasswordError')
    assert 'do not match' in page.inner_text('#confirmPasswordError')

@pytest.mark.e2e
def test_login_with_wrong_password(page, fastapi_server):
    """
    Negative test: Login with wrong password.
    Should return 401, UI shows invalid credentials message.
    """
    # First, register a user
    page.goto('http://localhost:8000/register')
    page.fill('#firstName', 'Login')
    page.fill('#lastName', 'Test')
    page.fill('#username', 'logintest')
    page.fill('#email', 'logintest@example.com')
    page.fill('#password', 'CorrectPassword123')
    page.fill('#confirmPassword', 'CorrectPassword123')
    page.click('button[type="submit"]')
    
    # Wait for registration to complete
    page.wait_for_selector('#successMessage', state='visible', timeout=10000)
    
    # Now navigate to login page
    page.goto('http://localhost:8000/login')
    
    # Fill in wrong login credentials
    page.fill('#username', 'logintest')
    page.fill('#password', 'WrongPassword123')  # Wrong password
    
    # Submit login form
    page.click('button[type="submit"]')
    
    # Wait for error message to appear
    page.wait_for_selector('#generalError', state='visible', timeout=10000)
    
    # Verify error message is displayed
    assert page.is_visible('#generalError')
    error_text = page.inner_text('#generalError')
    assert 'Invalid credentials' in error_text or 'Incorrect username or password' in error_text

@pytest.mark.e2e
def test_login_with_nonexistent_user(page, fastapi_server):
    """
    Negative test: Login with nonexistent username.
    Should return 401, UI shows invalid credentials message.
    """
    # Navigate to login page
    page.goto('http://localhost:8000/login')
    
    # Fill in nonexistent user credentials
    page.fill('#username', 'nonexistentuser')
    page.fill('#password', 'SomePassword123')
    
    # Submit login form
    page.click('button[type="submit"]')
    
    # Wait for error message to appear
    page.wait_for_selector('#generalError', state='visible', timeout=10000)
    
    # Verify error message is displayed
    assert page.is_visible('#generalError')
    error_text = page.inner_text('#generalError')
    assert 'Invalid credentials' in error_text or 'Incorrect username or password' in error_text

@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """
    Test the divide by zero functionality of the calculator.

    This test simulates a user attempting to divide a number by zero using the calculator
    on the frontend. It fills in two numbers (where the second is zero), clicks the "Divide"
    button, and verifies that an appropriate error message is displayed.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '0', attempting to divide by zero.
    page.fill('#b', '0')
    
    # Click the button that has the exact text "Divide". This triggers the division operation.
    page.click('button:text("Divide")')
    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly
    # "Error: Cannot divide by zero!". This verifies that the application handles division by zero
    # gracefully and displays the correct error message to the user.
    assert page.inner_text('#result') == 'Error: Cannot divide by zero!'
    """
    Test the divide by zero functionality of the calculator.

    This test simulates a user attempting to divide a number by zero using the calculator.
    It fills in the numbers, clicks the "Divide" button, and verifies that the appropriate
    error message is displayed. This ensures that the application correctly handles invalid
    operations and provides meaningful feedback to the user.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '0', attempting to divide by zero.
    page.fill('#b', '0')
    
    # Click the button that has the exact text "Divide". This triggers the division operation.
    page.click('button:text("Divide")')
    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly
    # "Error: Cannot divide by zero!". This verifies that the application handles division by zero
    # gracefully and displays the correct error message to the user.
    assert page.inner_text('#result') == 'Error: Cannot divide by zero!'
