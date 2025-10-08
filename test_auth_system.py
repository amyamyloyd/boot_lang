"""
Comprehensive authentication system test script.

Tests all authentication endpoints and workflows:
- User registration
- User login
- Protected endpoints
- Password changes
- Profile updates
- Admin operations
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    """Print success message in green."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Print error message in red."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    """Print info message in blue."""
    print(f"{Colors.BLUE}→ {message}{Colors.END}")

def print_section(title):
    """Print section header."""
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{Colors.END}\n")

def test_registration():
    """Test user registration endpoint."""
    print_section("TEST 1: User Registration")
    
    # Test successful registration
    print_info("Testing registration with valid data...")
    response = requests.post(f"{API_URL}/api/auth/register", json={
        "username": "testuser",
        "password": "test1234",
        "email": "test@example.com"
    })
    
    if response.status_code == 201:
        data = response.json()
        if data.get("success") and data.get("token"):
            print_success("Registration successful")
            print_success(f"User ID: {data['user']['id']}")
            print_success(f"Token received: {data['token'][:20]}...")
            return data['token'], data['user']['id']
        else:
            print_error("Registration response missing required fields")
            return None, None
    elif response.status_code == 400 and "already exists" in response.text:
        print_info("User already exists, proceeding to login...")
        return None, None
    else:
        print_error(f"Registration failed: {response.status_code}")
        print_error(response.text)
        return None, None

def test_login():
    """Test user login endpoint."""
    print_section("TEST 2: User Login")
    
    print_info("Testing login with valid credentials...")
    response = requests.post(f"{API_URL}/api/auth/login", json={
        "username": "testuser",
        "password": "test1234"
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("token"):
            print_success("Login successful")
            print_success(f"User: {data['user']['username']}")
            print_success(f"Admin: {data['user']['is_admin']}")
            return data['token'], data['user']['id']
        else:
            print_error("Login response missing required fields")
            return None, None
    else:
        print_error(f"Login failed: {response.status_code}")
        print_error(response.text)
        return None, None

def test_protected_endpoint(token):
    """Test protected endpoint with JWT token."""
    print_section("TEST 3: Protected Endpoint (Get Current User)")
    
    print_info("Testing /api/auth/me with valid token...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/api/auth/me", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Protected endpoint accessed successfully")
        print_success(f"Username: {data['username']}")
        print_success(f"Email: {data['email']}")
        print_success(f"Created: {data['created_at']}")
        return True
    else:
        print_error(f"Protected endpoint failed: {response.status_code}")
        print_error(response.text)
        return False

def test_invalid_token():
    """Test protected endpoint with invalid token."""
    print_section("TEST 4: Invalid Token Handling")
    
    print_info("Testing /api/auth/me with invalid token...")
    headers = {"Authorization": "Bearer invalid-token-12345"}
    response = requests.get(f"{API_URL}/api/auth/me", headers=headers)
    
    if response.status_code == 401:
        print_success("Invalid token correctly rejected")
        return True
    else:
        print_error(f"Expected 401, got {response.status_code}")
        return False

def test_password_change(token):
    """Test password change endpoint."""
    print_section("TEST 5: Password Change")
    
    print_info("Testing password change...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{API_URL}/api/user/password",
        headers=headers,
        json={
            "current_password": "test1234",
            "new_password": "newpass1234"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_success("Password changed successfully")
            
            # Try logging in with new password
            print_info("Verifying new password works...")
            login_response = requests.post(f"{API_URL}/api/auth/login", json={
                "username": "testuser",
                "password": "newpass1234"
            })
            
            if login_response.status_code == 200:
                print_success("Login with new password successful")
                
                # Change back to original password
                print_info("Changing password back to original...")
                new_token = login_response.json()['token']
                headers = {"Authorization": f"Bearer {new_token}"}
                requests.put(
                    f"{API_URL}/api/user/password",
                    headers=headers,
                    json={
                        "current_password": "newpass1234",
                        "new_password": "test1234"
                    }
                )
                print_success("Password restored to original")
                return True
            else:
                print_error("New password doesn't work")
                return False
        else:
            print_error("Password change response indicated failure")
            return False
    else:
        print_error(f"Password change failed: {response.status_code}")
        print_error(response.text)
        return False

def test_profile_update(token):
    """Test profile update endpoint."""
    print_section("TEST 6: Profile Update")
    
    print_info("Testing profile update...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Update email
    response = requests.put(
        f"{API_URL}/api/user/profile",
        headers=headers,
        json={"email": "newemail@example.com"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data['user']['email'] == "newemail@example.com":
            print_success("Profile updated successfully")
            print_success(f"New email: {data['user']['email']}")
            
            # Restore original email
            print_info("Restoring original email...")
            requests.put(
                f"{API_URL}/api/user/profile",
                headers=headers,
                json={"email": "test@example.com"}
            )
            print_success("Email restored")
            return True
        else:
            print_error("Profile update response incorrect")
            return False
    else:
        print_error(f"Profile update failed: {response.status_code}")
        print_error(response.text)
        return False

def create_admin_user():
    """Create an admin user for testing admin endpoints."""
    print_section("SETUP: Creating Admin User")
    
    from database import SessionLocal, User
    from auth_utils import hash_password
    
    db = SessionLocal()
    try:
        # Check if admin exists
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print_info("Admin user already exists")
            return True
        
        # Create admin user
        admin = User(
            username="admin",
            password_hash=hash_password("admin1234"),
            email="admin@bootlang.com",
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print_success("Admin user created")
        print_info("Username: admin")
        print_info("Password: admin1234")
        return True
    except Exception as e:
        print_error(f"Failed to create admin: {e}")
        return False
    finally:
        db.close()

def test_admin_list_users(admin_token):
    """Test admin list users endpoint."""
    print_section("TEST 7: Admin - List Users")
    
    print_info("Testing admin user list...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{API_URL}/api/admin/users", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("users"):
            print_success(f"User list retrieved: {len(data['users'])} users")
            return True
        else:
            print_error("Invalid response format")
            return False
    else:
        print_error(f"List users failed: {response.status_code}")
        return False

def test_admin_create_user(admin_token):
    """Test admin create user endpoint."""
    print_section("TEST 8: Admin - Create User")
    
    print_info("Testing admin user creation...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(
        f"{API_URL}/api/admin/users",
        headers=headers,
        json={
            "username": "admintest_user",
            "password": "test1234",
            "email": "admintest@example.com",
            "is_admin": False
        }
    )
    
    if response.status_code == 201 or (response.status_code == 400 and "already exists" in response.text):
        if response.status_code == 201:
            print_success("Admin created user successfully")
        else:
            print_info("User already exists")
        return True
    else:
        print_error(f"Admin create user failed: {response.status_code}")
        print_error(response.text)
        return False

def main():
    """Run all tests."""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("BOOT_LANG AUTHENTICATION SYSTEM TEST")
    print(f"{'='*60}{Colors.END}")
    print(f"API URL: {API_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test 1: Registration
    token, user_id = test_registration()
    if not token:
        # If registration failed (user exists), try login
        token, user_id = test_login()
    results['registration'] = token is not None
    
    if not token:
        print_error("Cannot proceed without valid token")
        return
    
    # Test 2: Login (if not already done)
    if 'login' not in results:
        _, _ = test_login()
        results['login'] = True
    
    # Test 3: Protected Endpoint
    results['protected'] = test_protected_endpoint(token)
    
    # Test 4: Invalid Token
    results['invalid_token'] = test_invalid_token()
    
    # Test 5: Password Change
    results['password_change'] = test_password_change(token)
    
    # Get fresh token after password change
    token, _ = test_login()
    
    # Test 6: Profile Update
    results['profile_update'] = test_profile_update(token)
    
    # Admin Tests
    if create_admin_user():
        # Login as admin
        print_section("SETUP: Admin Login")
        print_info("Logging in as admin...")
        admin_response = requests.post(f"{API_URL}/api/auth/login", json={
            "username": "admin",
            "password": "admin1234"
        })
        
        if admin_response.status_code == 200:
            admin_token = admin_response.json()['token']
            print_success("Admin login successful")
            
            # Test 7: List Users
            results['admin_list'] = test_admin_list_users(admin_token)
            
            # Test 8: Create User
            results['admin_create'] = test_admin_create_user(admin_token)
        else:
            print_error("Admin login failed")
            results['admin_list'] = False
            results['admin_create'] = False
    
    # Print Summary
    print_section("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    if failed > 0:
        print(f"{Colors.RED}Failed: {failed}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    if failed == 0:
        print_success("ALL TESTS PASSED! Authentication system is working correctly.")
    else:
        print_error(f"{failed} test(s) failed. Please review the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API server!")
        print_info("Make sure the backend is running on http://localhost:8000")
        print_info("Run: python3 app.py")
        exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

