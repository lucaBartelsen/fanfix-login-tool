from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    NORMAL = "normal"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.NORMAL)

    credentials = relationship("Credential", back_populates="owner")
    credential_assignments = relationship("CredentialAssignment", back_populates="user")