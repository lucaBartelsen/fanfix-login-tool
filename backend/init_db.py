from sqlalchemy.orm import Session
from app.models.base import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.credential import Credential
from app.core.security import get_password_hash, encrypt_password
from cryptography.fernet import Fernet

Base.metadata.create_all(bind=engine)


def init_db():
    db = SessionLocal()
    
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user created with username: admin, password: admin123")
    
    test_credential = db.query(Credential).filter(Credential.username == "kelly@unleashmgmt.family").first()
    if not test_credential:
        test_credential = Credential(
            name="Kelly Test Account",
            username="kelly@unleashmgmt.family",
            encrypted_password=encrypt_password("kersdd76_a9s8"),
            owner_id=admin_user.id
        )
        db.add(test_credential)
        db.commit()
        print("Test credential created")
    
    db.close()


def generate_encryption_key():
    key = Fernet.generate_key()
    print(f"Generated encryption key: {key.decode()}")
    print("Add this to your .env file as ENCRYPTION_KEY")


if __name__ == "__main__":
    print("Generating encryption key...")
    generate_encryption_key()
    print("\nInitializing database...")
    init_db()
    print("Database initialized successfully!")