from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String)
    encrypted_password = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="credentials")
    assignments = relationship("CredentialAssignment", back_populates="credential", cascade="all, delete-orphan")


class CredentialAssignment(Base):
    __tablename__ = "credential_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    credential_id = Column(Integer, ForeignKey("credentials.id"))
    assigned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="credential_assignments")
    credential = relationship("Credential", back_populates="assignments")