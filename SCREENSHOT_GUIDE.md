# Manual Screenshot Guide for BREAD Operations

This guide will help you capture screenshots demonstrating all BREAD (Browse, Read, Edit, Add, Delete) operations for your Module 14 assignment.

## Prerequisites

1. **Start your FastAPI server:**
   ```bash
   cd /Users/emisk/is218/module14_is218
   export DATABASE_URL='sqlite:///./test.db'
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Open your browser** to http://localhost:8000

3. **Screenshots folder is ready:** `screenshots/` (already created)

## 🔧 Important Setup Notes

- ✅ **Database tables are initialized** - Ready for user registration
- ✅ **Registration form now includes First Name and Last Name** - All required fields present
- ✅ **Authentication is working** - Users can register and login successfully
- ✅ **BREAD operations are user-specific** - Each user only sees their own calculations
- ✅ **Password Fixed**: Simple 3+ character password works (bcrypt issue resolved)

## Screenshot Sequence

### 1. Initial Interface (01_initial_interface.png)
- Navigate to http://localhost:8000
- Take a screenshot showing the complete interface
- **Shows:** Registration form, login form, basic calculator

### 2. User Registration (02_registration_demo.png)
- Fill out the registration form with **ALL REQUIRED FIELDS**:
  - **First Name:** `Demo`
  - **Last Name:** `User`  
  - **Username:** `demo` (or `demo2`, `demo3` if username exists)
  - **Email:** `demo@test.com`
  - **Password:** `pass` (simple 4-character password - bcrypt issue fixed)
- Click "Register" button
- Take screenshot showing successful registration message: "Registration successful! Please login."

✅ **Password issues resolved** - Any password should work now!

### 3. User Login (03_login_demo.png)
- Fill out the login form with same credentials:
  - **Username:** `demo`
  - **Password:** `pass`
- Click "Login" button
- Take screenshot showing successful login with the main calculator interface visible
- **Verify:** Auth forms disappear and main content with "Welcome! You are logged in." message appears

### 4. ADD Operation - Create Calculation (04_add_calculation.png)
- In the "Add Calculation" section:
  - First Number: `25`
  - Second Number: `5`
  - Operation: Select "Multiply"
- Click "Add Calculation"
- Take screenshot showing the successful creation message

### 5. BROWSE Operation - List All Calculations (05_browse_calculations.png)
- Click "Refresh Calculations" button
- Take screenshot showing the list of calculations
- **Shows:** All user's calculations in a table/list format

### 6. READ Operation - Get Specific Calculation (06_read_calculation.png)
- In the "Search by ID" section:
  - Enter `1` in the ID field
- Click "Search by ID"
- Take screenshot showing the specific calculation details

### 7. EDIT Operation - Update Calculation (07_edit_calculation.png)
- Click "Refresh Calculations" to see all calculations
- Click "Edit" button on any calculation
- Modify the values (e.g., change first number to `30`)
- Click "Update" button
- Take screenshot showing the updated calculation

### 8. Basic Calculator Demo (08_basic_calculator.png)
- In the "Basic Calculator" section:
  - First Number: `100`
  - Second Number: `25`
  - Operation: Select "Divide"
- Click "Calculate"
- Take screenshot showing the calculation result

### 9. DELETE Operation (09_delete_calculation.png)
- Click "Refresh Calculations" to see current calculations
- Click "Delete" button on any calculation
- Confirm the deletion
- Take screenshot showing the calculation has been removed

### 10. Error Handling Demo (10_error_handling.png)
- Try to create an invalid calculation (division by zero):
  - **First Number:** `10`
  - **Second Number:** `0`
  - **Operation:** "Divide"
- Click "Add Calculation" 
- Take screenshot showing the error message
- **Alternative:** Use Basic Calculator section to divide by zero and capture error
- **Expected:** Error message about division by zero should appear

### 11. Final Overview (11_final_overview.png)
- Take a final screenshot showing the complete interface
- Should show remaining calculations and all interface sections

## 📸 Screenshot Tips

1. **Use full-page screenshots** to show the complete interface
2. **Make browser window wide enough** (at least 1200px) for good visibility  
3. **Ensure all text is readable** - zoom to 100% or 110% if needed
4. **Include browser URL bar** to show you're accessing localhost:8000
5. **Save with descriptive filenames** as suggested above
6. **Wait for responses** - Allow time for server responses before taking screenshots
7. **Show success messages** - Capture confirmation messages after operations
8. **Refresh between operations** - Click "Refresh Calculations" to see updated data

## ⚡ Quick Start Commands

**Terminal 1 - Start Server:**
```bash
cd /Users/emisk/is218/module14_is218
export DATABASE_URL='sqlite:///./test.db'
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 - Quick Test (optional):**
```bash
# Test if server is responding
curl -s http://localhost:8000 | head -5
```

## Verification Checklist

✅ **CREATE (Add)** - Screenshot shows successful calculation creation  
✅ **READ (Browse)** - Screenshot shows list of all calculations  
✅ **READ (Individual)** - Screenshot shows specific calculation details  
✅ **UPDATE (Edit)** - Screenshot shows successful calculation modification  
✅ **DELETE** - Screenshot shows calculation removal  
✅ **Authentication** - Screenshots show login/registration working  
✅ **Error Handling** - Screenshot shows proper error messages  
✅ **UI/UX** - Screenshots demonstrate responsive, user-friendly interface

## File Organization

Save all screenshots in a `screenshots/` folder with clear naming:
```
screenshots/
├── 01_initial_interface.png
├── 02_registration_demo.png
├── 03_login_demo.png
├── 04_add_calculation.png
├── 05_browse_calculations.png
├── 06_read_calculation.png
├── 07_edit_calculation.png
├── 08_basic_calculator.png
├── 09_delete_calculation.png
├── 10_error_handling.png
└── 11_final_overview.png
```

## 🎯 Success Checklist

After taking all screenshots, verify you have captured:

- ✅ **Authentication Flow:** Registration with all fields → Login → Access granted
- ✅ **CREATE (Add):** New calculation added with confirmation message
- ✅ **READ (Browse):** List of all user's calculations displayed  
- ✅ **READ (Individual):** Specific calculation details shown via ID search
- ✅ **UPDATE (Edit):** Calculation modified with updated values displayed
- ✅ **DELETE:** Calculation removed and no longer appears in list
- ✅ **Error Handling:** Division by zero or other errors properly handled
- ✅ **User Experience:** Clean interface, responsive design, clear feedback
- ✅ **Security:** User-specific data (each user sees only their calculations)

## 🚀 Assignment Completion

These screenshots will demonstrate that your Module 14 assignment fully implements:
- **BREAD operations** for calculations with proper authentication
- **User management** with registration and login
- **Data security** with user-specific calculation access  
- **Error handling** and user-friendly interface
- **Full-stack implementation** with FastAPI backend and responsive frontend

**Your assignment is complete and ready for submission!** 🎉