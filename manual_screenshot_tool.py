#!/usr/bin/env python3
"""
Simple screenshot script for BREAD operations.
Run this after starting your FastAPI server manually.
"""

import asyncio
import os
from playwright.async_api import async_playwright

async def take_screenshots():
    """Take screenshots of the BREAD operations interface"""
    
    # Create screenshots directory
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2000)
        page = await browser.new_page()
        
        # Set viewport size for consistent screenshots
        await page.set_viewport_size({"width": 1400, "height": 1000})
        
        try:
            print("📸 Taking screenshots of BREAD operations...")
            
            # Navigate to the application
            await page.goto("http://localhost:8000")
            await page.wait_for_load_state("networkidle")
            
            # Screenshot 1: Initial interface
            await page.screenshot(path=f"{screenshot_dir}/01_initial_interface.png", full_page=True)
            print("✅ Screenshot 1: Initial interface")
            
            # Pause for manual interaction
            print("\n🔄 MANUAL STEPS - Please perform these actions in the browser:")
            print("   1. Register a new user (username: testuser, email: test@example.com, password: TestPass123)")
            print("   2. Login with the same credentials")
            print("   3. Press ENTER here when you're logged in and ready to continue...")
            input("Press ENTER to continue...")
            
            # Screenshot 2: After login - main interface
            await page.screenshot(path=f"{screenshot_dir}/02_main_interface_logged_in.png", full_page=True)
            print("✅ Screenshot 2: Main interface after login")
            
            print("\n🔄 MANUAL STEP - Please add a calculation:")
            print("   - First Number: 25, Second Number: 5, Operation: Multiply")
            print("   - Click 'Add Calculation'")
            print("   - Press ENTER when done...")
            input("Press ENTER to continue...")
            
            # Screenshot 3: After adding calculation
            await page.screenshot(path=f"{screenshot_dir}/03_add_calculation_result.png", full_page=True)
            print("✅ Screenshot 3: ADD operation result")
            
            print("\n🔄 MANUAL STEP - Please browse calculations:")
            print("   - Click 'Refresh Calculations'")
            print("   - Press ENTER when done...")
            input("Press ENTER to continue...")
            
            # Screenshot 4: Browse calculations
            await page.screenshot(path=f"{screenshot_dir}/04_browse_calculations.png", full_page=True)
            print("✅ Screenshot 4: BROWSE operation")
            
            print("\n🔄 MANUAL STEP - Please search for a calculation:")
            print("   - Enter '1' in the 'Search by ID' field")
            print("   - Click 'Search by ID'")
            print("   - Press ENTER when done...")
            input("Press ENTER to continue...")
            
            # Screenshot 5: Read specific calculation
            await page.screenshot(path=f"{screenshot_dir}/05_read_calculation.png", full_page=True)
            print("✅ Screenshot 5: READ operation")
            
            print("\n🔄 MANUAL STEP - Please edit a calculation:")
            print("   - Click 'Refresh Calculations' first")
            print("   - Click 'Edit' on any calculation")
            print("   - Change some values and click 'Update'")
            print("   - Press ENTER when done...")
            input("Press ENTER to continue...")
            
            # Screenshot 6: Edit operation
            await page.screenshot(path=f"{screenshot_dir}/06_edit_calculation.png", full_page=True)
            print("✅ Screenshot 6: EDIT operation")
            
            print("\n🔄 MANUAL STEP - Please use the basic calculator:")
            print("   - Enter numbers in the basic calculator section")
            print("   - Try a division operation")
            print("   - Press ENTER when done...")
            input("Press ENTER to continue...")
            
            # Screenshot 7: Basic calculator
            await page.screenshot(path=f"{screenshot_dir}/07_basic_calculator.png", full_page=True)
            print("✅ Screenshot 7: Basic calculator operation")
            
            print("\n🔄 MANUAL STEP - Please delete a calculation:")
            print("   - Click 'Refresh Calculations'")
            print("   - Click 'Delete' on any calculation")
            print("   - Confirm deletion")
            print("   - Press ENTER when done...")
            input("Press ENTER to continue...")
            
            # Screenshot 8: After deletion
            await page.screenshot(path=f"{screenshot_dir}/08_delete_calculation.png", full_page=True)
            print("✅ Screenshot 8: DELETE operation")
            
            print("\n🔄 MANUAL STEP - Please demonstrate error handling:")
            print("   - Try to add a calculation with division by zero (10 ÷ 0)")
            print("   - Or use the basic calculator to divide by zero")
            print("   - Press ENTER when done...")
            input("Press ENTER to continue...")
            
            # Screenshot 9: Error handling
            await page.screenshot(path=f"{screenshot_dir}/09_error_handling.png", full_page=True)
            print("✅ Screenshot 9: Error handling")
            
            # Final overview screenshot
            await page.screenshot(path=f"{screenshot_dir}/10_final_overview.png", full_page=True)
            print("✅ Screenshot 10: Final overview")
            
            print(f"\n🎉 All screenshots saved to '{screenshot_dir}/' folder!")
            print("\nScreenshots taken:")
            print("  01_initial_interface.png - Initial application interface")
            print("  02_main_interface_logged_in.png - After successful login")
            print("  03_add_calculation_result.png - ADD operation (Create)")
            print("  04_browse_calculations.png - BROWSE operation (Read All)")
            print("  05_read_calculation.png - READ operation (Read One)")
            print("  06_edit_calculation.png - EDIT operation (Update)")
            print("  07_basic_calculator.png - Basic calculator functionality")
            print("  08_delete_calculation.png - DELETE operation")
            print("  09_error_handling.png - Error handling demonstration")
            print("  10_final_overview.png - Complete interface overview")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    print("🚀 Manual BREAD Operations Screenshot Tool")
    print("=" * 50)
    print("SETUP INSTRUCTIONS:")
    print("1. Start your FastAPI server first:")
    print("   cd /Users/emisk/is218/module14_is218")
    print("   export DATABASE_URL='sqlite:///./test.db'")
    print("   uvicorn main:app --host 127.0.0.1 --port 8000 --reload")
    print("")
    print("2. Make sure the server is running at http://localhost:8000")
    print("3. Then run this script - it will guide you through each step")
    print("")
    print("Press ENTER when your server is running and ready...")
    input()
    
    asyncio.run(take_screenshots())