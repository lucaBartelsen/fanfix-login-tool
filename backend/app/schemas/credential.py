from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CredentialBase(BaseModel):
    name: str
    username: str


class CredentialCreate(CredentialBase):
    password: str


class CredentialUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class Credential(CredentialBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CredentialWithPassword(Credential):
    password: str


class CredentialAssign(BaseModel):
    user_ids: List[int]