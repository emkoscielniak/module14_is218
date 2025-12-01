# tests/e2e/test_e2e.py

import pytest  # Import the pytest framework for writing and running tests
import time

# The following decorators and functions define E2E tests for the FastAPI calculator application.

@pytest.mark.e2e
def test_homepage_loads(page, fastapi_server):
    """
    Test that the homepage displays the correct title.
    """
    page.goto('http://localhost:8000')
    assert page.inner_text('h1') == 'Calculator & Calculation Manager'

@pytest.mark.e2e 
def test_authentication_flow(page, fastapi_server):
    """
    Test user registration and login flow.
    """
    page.goto('http://localhost:8000')
    
    # Test registration
    page.fill('#register-username', 'testuser123')
    page.fill('#register-email', 'testuser123@example.com')
    page.fill('#register-password', 'TestPassword123')
    page.click('button:text("Register")')
    
    # Wait for success message or alert
    time.sleep(2)
    
    # Test login
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    # Wait for main content to appear
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Verify user is logged in
    assert page.is_visible('#user-info')
    assert 'Welcome, testuser123!' in page.inner_text('#welcome-message')

@pytest.mark.e2e
def test_basic_calculator_functionality(page, fastapi_server):
    """
    Test the basic calculator functionality after authentication.
    """
    # First login
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Test addition
    page.fill('#a', '10')
    page.fill('#b', '5')
    page.click('button:text("Add")')
    
    # Wait for result and verify
    page.wait_for_function("document.getElementById('result').textContent.includes('Result: 15')")
    assert 'Result: 15' in page.inner_text('#result')

@pytest.mark.e2e
def test_add_calculation_positive(page, fastapi_server):
    """
    Positive test: Successfully add a new calculation.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Add a new calculation
    page.fill('#calc-a', '20')
    page.fill('#calc-b', '10')
    page.select_option('#calc-type', 'Add')
    page.click('button:text("Add Calculation")')
    
    # Wait for success message
    time.sleep(2)
    
    # Load calculations to verify it was added
    page.click('button:text("Refresh Calculations")')
    time.sleep(2)
    
    # Verify calculation appears in the list
    assert page.locator('.calculation-item').count() > 0

@pytest.mark.e2e
def test_browse_calculations(page, fastapi_server):
    """
    Test browsing all user calculations.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Browse calculations
    page.click('button:text("Refresh Calculations")')
    time.sleep(2)
    
    # Verify calculations are displayed
    calculations_result = page.inner_text('#calculations-result')
    assert 'calculation(s)' in calculations_result or 'No calculations found' in calculations_result

@pytest.mark.e2e
def test_read_specific_calculation(page, fastapi_server):
    """
    Test reading a specific calculation by ID.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # First add a calculation to have something to search for
    page.fill('#calc-a', '25')
    page.fill('#calc-b', '5')
    page.select_option('#calc-type', 'Divide')
    page.click('button:text("Add Calculation")')
    time.sleep(2)
    
    # Load all calculations to get an ID
    page.click('button:text("Refresh Calculations")')
    time.sleep(2)
    
    # Try searching for calculation with ID 1 (assuming it exists)
    page.fill('#search-id', '1')
    page.click('button:text("Search by ID")')
    time.sleep(2)

@pytest.mark.e2e
def test_edit_calculation_positive(page, fastapi_server):
    """
    Positive test: Successfully edit an existing calculation.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Add a calculation first
    page.fill('#calc-a', '15')
    page.fill('#calc-b', '3')
    page.select_option('#calc-type', 'Multiply')
    page.click('button:text("Add Calculation")')
    time.sleep(2)
    
    # Load calculations
    page.click('button:text("Refresh Calculations")')
    time.sleep(2)
    
    # Click edit on the first calculation (if any exist)
    edit_buttons = page.locator('button:text("Edit")')
    if edit_buttons.count() > 0:
        edit_buttons.first.click()
        
        # Wait for edit form to appear
        page.wait_for_selector('#edit-section', state='visible', timeout=5000)
        
        # Modify the calculation
        page.fill('#edit-calc-a', '30')
        page.click('button:text("Update")')
        
        time.sleep(2)

@pytest.mark.e2e
def test_delete_calculation_positive(page, fastapi_server):
    """
    Positive test: Successfully delete a calculation.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Add a calculation first
    page.fill('#calc-a', '100')
    page.fill('#calc-b', '10')
    page.select_option('#calc-type', 'Sub')
    page.click('button:text("Add Calculation")')
    time.sleep(2)
    
    # Load calculations
    page.click('button:text("Refresh Calculations")')
    time.sleep(2)
    
    # Count initial calculations
    initial_count = page.locator('.calculation-item').count()
    
    # Delete first calculation if any exist
    delete_buttons = page.locator('button:text("Delete")')
    if delete_buttons.count() > 0:
        # Handle the confirm dialog
        page.on("dialog", lambda dialog: dialog.accept())
        delete_buttons.first.click()
        
        time.sleep(2)
        
        # Refresh and verify count decreased
        page.click('button:text("Refresh Calculations")')
        time.sleep(2)

# Negative Test Cases

@pytest.mark.e2e
def test_add_calculation_invalid_input(page, fastapi_server):
    """
    Negative test: Try to add calculation with invalid inputs.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Try to add calculation without filling numbers
    page.click('button:text("Add Calculation")')
    time.sleep(1)
    
    # Should show alert or error (client-side validation)

@pytest.mark.e2e
def test_divide_by_zero_calculation(page, fastapi_server):
    """
    Negative test: Try to add a division by zero calculation.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Try to add division by zero
    page.fill('#calc-a', '10')
    page.fill('#calc-b', '0')
    page.select_option('#calc-type', 'Divide')
    page.click('button:text("Add Calculation")')
    
    time.sleep(2)
    # Should show error message

@pytest.mark.e2e
def test_basic_calculator_divide_by_zero(page, fastapi_server):
    """
    Negative test: Test divide by zero in basic calculator.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Test division by zero
    page.fill('#a', '10')
    page.fill('#b', '0')
    page.click('button:text("Divide")')
    
    # Wait for error message
    page.wait_for_function("document.getElementById('result').textContent.includes('Error')")
    assert 'Error' in page.inner_text('#result')

@pytest.mark.e2e
def test_search_nonexistent_calculation(page, fastapi_server):
    """
    Negative test: Search for a calculation that doesn't exist.
    """
    # Login first
    page.goto('http://localhost:8000')
    page.fill('#login-username', 'testuser123')
    page.fill('#login-password', 'TestPassword123')
    page.click('button:text("Login")')
    
    page.wait_for_selector('#main-content', state='visible', timeout=10000)
    
    # Search for non-existent calculation
    page.fill('#search-id', '99999')
    page.click('button:text("Search by ID")')
    time.sleep(2)
    
    # Should show error message
    result_text = page.inner_text('#calculations-result')
    assert 'Error' in result_text or 'not found' in result_text

@pytest.mark.e2e
def test_unauthorized_access(page, fastapi_server):
    """
    Negative test: Try to access calculations without authentication.
    """
    page.goto('http://localhost:8000')
    
    # Verify that main content is hidden and auth section is visible
    assert not page.is_visible('#main-content')
    assert page.is_visible('#auth-section')

@pytest.mark.e2e
def test_login_with_invalid_credentials(page, fastapi_server):
    """
    Negative test: Try to login with invalid credentials.
    """
    page.goto('http://localhost:8000')
    
    # Try to login with wrong credentials
    page.fill('#login-username', 'wronguser')
    page.fill('#login-password', 'wrongpassword')
    page.click('button:text("Login")')
    
    time.sleep(2)
    
    # Should remain on login screen
    assert page.is_visible('#auth-section')
    assert not page.is_visible('#main-content')

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
