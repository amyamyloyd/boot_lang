"""
Database test script to verify database setup and basic operations.

This script:
1. Initializes the database
2. Creates a test user
3. Queries the user back
4. Verifies password hashing
5. Prints success message
"""

from database import init_db, SessionLocal, User
from auth_utils import hash_password, verify_password

def test_database():
    """Test database initialization and basic operations."""
    print("=" * 60)
    print("DATABASE TEST SCRIPT")
    print("=" * 60)
    
    # Step 1: Initialize database
    print("\n[1/5] Initializing database...")
    init_db()
    
    # Step 2: Create database session
    print("\n[2/5] Creating database session...")
    db = SessionLocal()
    
    try:
        # Step 3: Create a test user
        print("\n[3/5] Creating test user...")
        test_username = "testuser"
        test_password = "testpass123"
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == test_username).first()
        if existing_user:
            print(f"   ⚠ User '{test_username}' already exists, deleting...")
            db.delete(existing_user)
            db.commit()
        
        # Hash password and create user
        hashed_pw = hash_password(test_password)
        new_user = User(
            username=test_username,
            email="test@example.com",
            password_hash=hashed_pw,
            is_admin=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"   ✓ Created user: {new_user}")
        
        # Step 4: Query the user back
        print("\n[4/5] Querying user from database...")
        queried_user = db.query(User).filter(User.username == test_username).first()
        
        if queried_user:
            print(f"   ✓ Found user: {queried_user}")
            print(f"     - ID: {queried_user.id}")
            print(f"     - Username: {queried_user.username}")
            print(f"     - Email: {queried_user.email}")
            print(f"     - Is Admin: {queried_user.is_admin}")
            print(f"     - Created: {queried_user.created_at}")
        else:
            print("   ✗ ERROR: User not found!")
            return False
        
        # Step 5: Verify password hashing
        print("\n[5/5] Testing password verification...")
        is_correct = verify_password(test_password, queried_user.password_hash)
        is_wrong = verify_password("wrongpassword", queried_user.password_hash)
        
        if is_correct and not is_wrong:
            print("   ✓ Password hashing working correctly")
        else:
            print("   ✗ ERROR: Password verification failed!")
            return False
        
        # Clean up test user
        print("\n[Cleanup] Removing test user...")
        db.delete(queried_user)
        db.commit()
        print("   ✓ Test user removed")
        
        # Success!
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nDatabase is ready for use.")
        print("You can now:")
        print("  1. Start the backend: python3 app.py")
        print("  2. Create users via API endpoints")
        print("  3. View boot_lang.db with SQLite browser")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    success = test_database()
    exit(0 if success else 1)

