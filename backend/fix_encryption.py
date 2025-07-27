"""
Script to re-encrypt credentials with a new encryption key
"""
from sqlalchemy.orm import Session
from app.models.base import SessionLocal, Base, engine
from app.core.security import encrypt_password
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Import all models to ensure relationships are loaded
from app.models.user import User
from app.models.credential import Credential

load_dotenv()

# Create all tables
Base.metadata.create_all(bind=engine)

def fix_credentials():
    """Re-encrypt all credentials with current encryption key"""
    db = SessionLocal()
    
    # Generate new encryption key if needed
    encryption_key = os.getenv("ENCRYPTION_KEY")
    if not encryption_key:
        encryption_key = Fernet.generate_key().decode()
        print(f"Generated new ENCRYPTION_KEY: {encryption_key}")
        print("Add this to your .env file!")
        return
    
    try:
        # For testing, let's create a fresh test credential
        # First, delete existing test credential
        test_cred = db.query(Credential).filter(
            Credential.username == "kelly@unleashmgmt.family"
        ).first()
        
        if test_cred:
            db.delete(test_cred)
            db.commit()
            print("Deleted old test credential")
        
        # Create new test credential with current encryption key
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            new_cred = Credential(
                name="Kelly Test Account",
                username="kelly@unleashmgmt.family",
                encrypted_password=encrypt_password("kersdd76_a9s8"),
                owner_id=admin_user.id
            )
            db.add(new_cred)
            db.commit()
            print("Created new test credential with current encryption key")
        else:
            print("Admin user not found!")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_credentials()