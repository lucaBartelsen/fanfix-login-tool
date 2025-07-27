from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import encrypt_password, decrypt_password
from app.dependencies import get_db, get_current_active_user, get_admin_user
from app.models.user import User, UserRole
from app.models.credential import Credential, CredentialAssignment
from app.schemas.credential import (
    Credential as CredentialSchema,
    CredentialCreate,
    CredentialUpdate,
    CredentialWithPassword,
    CredentialAssign
)

router = APIRouter()


@router.post("/", response_model=CredentialSchema)
async def create_credential(
    credential: CredentialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    db_credential = Credential(
        name=credential.name,
        username=credential.username,
        encrypted_password=encrypt_password(credential.password),
        owner_id=current_user.id
    )
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential


@router.get("/", response_model=List[CredentialSchema])
async def read_credentials(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role == UserRole.ADMIN:
        credentials = db.query(Credential).offset(skip).limit(limit).all()
    else:
        credential_ids = [ca.credential_id for ca in current_user.credential_assignments]
        credentials = db.query(Credential).filter(Credential.id.in_(credential_ids)).offset(skip).limit(limit).all()
    return credentials


@router.get("/{credential_id}", response_model=CredentialWithPassword)
async def read_credential(
    credential_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    if current_user.role != UserRole.ADMIN:
        assignment = db.query(CredentialAssignment).filter(
            CredentialAssignment.user_id == current_user.id,
            CredentialAssignment.credential_id == credential_id
        ).first()
        if not assignment:
            raise HTTPException(status_code=403, detail="Not authorized to access this credential")
    
    return {
        **credential.__dict__,
        "password": decrypt_password(credential.encrypted_password)
    }


@router.patch("/{credential_id}", response_model=CredentialSchema)
async def update_credential(
    credential_id: int,
    credential_update: CredentialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    update_data = credential_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["encrypted_password"] = encrypt_password(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(credential, field, value)
    
    db.commit()
    db.refresh(credential)
    return credential


@router.delete("/{credential_id}")
async def delete_credential(
    credential_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    db.delete(credential)
    db.commit()
    return {"message": "Credential deleted successfully"}


@router.post("/{credential_id}/assign")
async def assign_credential(
    credential_id: int,
    assignment: CredentialAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    credential = db.query(Credential).filter(Credential.id == credential_id).first()
    if credential is None:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    db.query(CredentialAssignment).filter(
        CredentialAssignment.credential_id == credential_id
    ).delete()
    
    for user_id in assignment.user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            continue
        
        db_assignment = CredentialAssignment(
            user_id=user_id,
            credential_id=credential_id
        )
        db.add(db_assignment)
    
    db.commit()
    return {"message": "Credential assignments updated successfully"}