"""Script to create admin user"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlmodel import Session
from forgeerp.core.database.database import engine, create_db_and_tables
from forgeerp.core.database.models.user import User
from forgeerp.core.services.authentication import get_password_hash

def create_admin_user(username: str = "admin", password: str = "admin", email: str = "admin@forgeerp.ai"):
    """Create admin user"""
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if user already exists
        from sqlmodel import select
        statement = select(User).where(User.username == username)
        existing = session.exec(statement).first()
        
        if existing:
            print(f"User '{username}' already exists!")
            return
        
        # Create admin user
        user = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password),
            full_name="Admin User",
            role="superuser",
            is_active=True,
            is_superuser=True,
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        print(f"Admin user '{username}' created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        print("\n⚠️  IMPORTANT: Change the password after first login!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create admin user")
    parser.add_argument("--username", default="admin", help="Username")
    parser.add_argument("--password", default="admin", help="Password")
    parser.add_argument("--email", default="admin@forgeerp.ai", help="Email")
    
    args = parser.parse_args()
    
    create_admin_user(args.username, args.password, args.email)

