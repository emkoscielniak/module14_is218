#!/usr/bin/env python3
"""
Automated screenshot generator for BREAD operations using Playwright.
This script will start the FastAPI server, perform all BREAD operations,
and take screenshots for assignment documentation.
"""

import asyncio
import subprocess
import time
import os
from playwright.async_api import async_playwright

class BREADScreenshotter:
    def __init__(self):
        self.server_process = None
        self.screenshot_dir = "screenshots"
        self.base_url = "http://localhost:8000"
        
    async def setup(self):
        """Setup screenshot directory and start server"""
        # Create screenshots directory
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Set environment variable for SQLite
        os.environ["DATABASE_URL"] = "sqlite:///./test.db"
        
        # Start FastAPI server
        print("Starting FastAPI server...")
        self.server_process = subprocess.Popen(
            ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        await asyncio.sleep(3)
        print("Server started!")
        
    async def cleanup(self):
        """Stop the server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("Server stopped!")
    
    async def take_screenshot(self, page, name, description):
        """Take a screenshot with description"""
        screenshot_path = f"{self.screenshot_dir}/{name}.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"✅ Screenshot saved: {name}.png - {description}")
        return screenshot_path
    
    async def run_bread_demo(self):
        """Run complete BREAD operations demo with screenshots"""
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=False, slow_mo=1000)
            page = await browser.new_page()
            
            try:
                # Screenshot 1: Initial page load
                print("Navigating to application...")
                await page.goto(self.base_url)
                await page.wait_for_load_state("networkidle")
                
                # Debug: Check what's on the page
                title = await page.title()
                print(f"Page title: {title}")
                
                await self.take_screenshot(page, "01_initial_page", 
                                         "Initial application page showing authentication interface")
                
                # Screenshot 2: User Registration
                # Wait for the registration form to be visible
                await page.wait_for_selector('#register-username', timeout=10000)
                await page.fill('#register-username', 'demouser')
                await page.fill('#register-email', 'demo@example.com')
                await page.fill('#register-password', 'DemoPass123')
                await self.take_screenshot(page, "02_registration_form", 
                                         "User registration form filled out")
                
                await page.click('button:text("Register")')
                await asyncio.sleep(2)  # Wait for registration
                await self.take_screenshot(page, "03_registration_success", 
                                         "Successful user registration")
                
                # Screenshot 3: User Login
                await page.fill('#login-username', 'demouser')
                await page.fill('#login-password', 'DemoPass123')
                await self.take_screenshot(page, "04_login_form", 
                                         "Login form with credentials")
                
                await page.click('button:text("Login")')
                await page.wait_for_selector('#main-content', state='visible')
                await self.take_screenshot(page, "05_successful_login", 
                                         "Successful login showing main interface")
                
                # Screenshot 4: ADD Operation (Create)
                await page.fill('#calc-a', '25')
                await page.fill('#calc-b', '5')
                await page.select_option('#calc-type', 'Multiply')
                await self.take_screenshot(page, "06_add_calculation_form", 
                                         "ADD operation - Creating new calculation")
                
                await page.click('button:text("Add Calculation")')
                await asyncio.sleep(2)
                await self.take_screenshot(page, "07_add_calculation_success", 
                                         "ADD operation - Calculation created successfully")
                
                # Add a few more calculations for better demo
                calculations = [
                    {'a': '100', 'b': '20', 'type': 'Divide'},
                    {'a': '15', 'b': '7', 'type': 'Add'},
                    {'a': '50', 'b': '12', 'type': 'Sub'}
                ]
                
                for calc in calculations:
                    await page.fill('#calc-a', calc['a'])
                    await page.fill('#calc-b', calc['b'])
                    await page.select_option('#calc-type', calc['type'])
                    await page.click('button:text("Add Calculation")')
                    await asyncio.sleep(1)
                
                # Screenshot 5: BROWSE Operation (Read All)
                await page.click('button:text("Refresh Calculations")')
                await asyncio.sleep(2)
                await self.take_screenshot(page, "08_browse_calculations", 
                                         "BROWSE operation - Viewing all user calculations")
                
                # Screenshot 6: READ Operation (Read One)
                await page.fill('#search-id', '1')
                await self.take_screenshot(page, "09_read_calculation_search", 
                                         "READ operation - Searching for specific calculation")
                
                await page.click('button:text("Search by ID")')
                await asyncio.sleep(2)
                await self.take_screenshot(page, "10_read_calculation_result", 
                                         "READ operation - Specific calculation details")
                
                # Refresh to show all calculations again
                await page.click('button:text("Refresh Calculations")')
                await asyncio.sleep(2)
                
                # Screenshot 7: EDIT Operation (Update)
                edit_buttons = page.locator('button:text("Edit")')
                if await edit_buttons.count() > 0:
                    await edit_buttons.first.click()
                    await page.wait_for_selector('#edit-section', state='visible')
                    await self.take_screenshot(page, "11_edit_calculation_form", 
                                             "EDIT operation - Editing existing calculation")
                    
                    # Modify the calculation
                    await page.fill('#edit-calc-a', '200')
                    await page.fill('#edit-calc-b', '10')
                    await self.take_screenshot(page, "12_edit_calculation_modified", 
                                             "EDIT operation - Modified calculation values")
                    
                    await page.click('button:text("Update")')
                    await asyncio.sleep(2)
                    await self.take_screenshot(page, "13_edit_calculation_success", 
                                             "EDIT operation - Calculation updated successfully")
                
                # Screenshot 8: Basic Calculator
                await page.fill('#a', '144')
                await page.fill('#b', '12')
                await self.take_screenshot(page, "14_basic_calculator_input", 
                                         "Basic calculator with input values")
                
                await page.click('button:text("Divide")')
                await asyncio.sleep(1)
                await self.take_screenshot(page, "15_basic_calculator_result", 
                                         "Basic calculator showing division result")
                
                # Screenshot 9: Error Handling (Division by Zero)
                await page.fill('#calc-a', '10')
                await page.fill('#calc-b', '0')
                await page.select_option('#calc-type', 'Divide')
                await page.click('button:text("Add Calculation")')
                await asyncio.sleep(2)
                await self.take_screenshot(page, "16_error_handling", 
                                         "Error handling - Division by zero validation")
                
                # Screenshot 10: DELETE Operation
                await page.click('button:text("Refresh Calculations")')
                await asyncio.sleep(2)
                
                # Handle the confirm dialog for deletion
                page.on("dialog", lambda dialog: dialog.accept())
                
                delete_buttons = page.locator('button:text("Delete")')
                if await delete_buttons.count() > 0:
                    await self.take_screenshot(page, "17_before_delete", 
                                             "DELETE operation - Before deleting calculation")
                    
                    await delete_buttons.first.click()
                    await asyncio.sleep(2)
                    
                    await page.click('button:text("Refresh Calculations")')
                    await asyncio.sleep(2)
                    await self.take_screenshot(page, "18_after_delete", 
                                             "DELETE operation - After deleting calculation")
                
                # Final screenshot showing complete interface
                await self.take_screenshot(page, "19_final_interface", 
                                         "Complete BREAD operations interface demonstration")
                
                print(f"\n🎉 All screenshots completed! Check the '{self.screenshot_dir}' folder.")
                
            except Exception as e:
                print(f"❌ Error during screenshot process: {e}")
                await self.take_screenshot(page, "error_state", f"Error state: {e}")
            
            finally:
                await browser.close()

async def main():
    screenshotter = BREADScreenshotter()
    
    try:
        await screenshotter.setup()
        await screenshotter.run_bread_demo()
    finally:
        await screenshotter.cleanup()

if __name__ == "__main__":
    print("🚀 Starting BREAD Operations Screenshot Generator")
    print("This will automatically demonstrate all BREAD operations and take screenshots.")
    print("Make sure you have Playwright installed: pip install playwright")
    print("And browser binaries: playwright install")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    asyncio.run(main())