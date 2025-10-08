"""
Create the first admin user for Boot_Lang.

Run this script to create an admin account that can access the admin panel.
"""

from database import init_db, SessionLocal, User
from auth_utils import hash_password

def create_admin():
    """Create admin user."""
    print("Creating admin user...")
    
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing = db.query(User).filter(User.username == "admin").first()
        
        if existing:
            print("\n⚠  Admin user already exists!")
            print(f"   Username: {existing.username}")
            print(f"   Is Admin: {existing.is_admin}")
            
            if not existing.is_admin:
                print("\n   Upgrading to admin privileges...")
                existing.is_admin = True
                db.commit()
                print("   ✓ User upgraded to admin")
        else:
            # Create admin user
            admin = User(
                username="admin",
                password_hash=hash_password("admin1234"),
                email="admin@bootlang.com",
                is_admin=True
            )
            
            db.add(admin)
            db.commit()
            db.refresh(admin)
            
            print("\n✓ Admin user created successfully!")
            print(f"   Username: {admin.username}")
            print(f"   Password: admin1234")
            print(f"   Email: {admin.email}")
            print(f"   User ID: {admin.id}")
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. Start the backend: python3 app.py")
        print("2. Start the frontend: cd frontend && npm start")
        print("3. Open browser: http://localhost:3000")
        print("4. Login with:")
        print("   - Username: admin")
        print("   - Password: admin1234")
        print("5. IMPORTANT: Change the password after first login!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = create_admin()
    exit(0 if success else 1)

