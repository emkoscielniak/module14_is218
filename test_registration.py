#!/usr/bin/env python3
"""
Simple test script to verify registration works
"""
import requests
import time

def test_registration():
    url = "http://127.0.0.1:8000/users/register"
    
    # Test data
    data = {
        "first_name": "Demo",
        "last_name": "User", 
        "username": "demotest",
        "email": "demo@test.com",
        "password": "pass"
    }
    
    try:
        print("🔹 Testing server connection...")
        response = requests.get("http://127.0.0.1:8000")
        if response.status_code == 200:
            print("✅ Server is responding")
        else:
            print(f"❌ Server error: {response.status_code}")
            return
            
        print("🔹 Testing user registration...")
        response = requests.post(url, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Registration successful!")
            
            # Test login
            print("🔹 Testing login...")
            login_data = {
                "username": "demotest",
                "password": "pass"
            }
            login_response = requests.post("http://127.0.0.1:8000/users/login", json=login_data)
            print(f"Login Status: {login_response.status_code}")
            print(f"Login Response: {login_response.text}")
            
            if login_response.status_code == 200:
                print("✅ Login successful!")
                print("\n🎉 Everything works! You can now use the web interface:")
                print("   Username: demotest")
                print("   Password: pass")
            else:
                print("❌ Login failed")
        else:
            print("❌ Registration failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration()