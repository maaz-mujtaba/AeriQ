# app/crud.py
from sqlalchemy.orm import Session
from typing import Optional, List
import json

from app.db_models import User
from app.models import UserCreate, UserUpdate  # ← Pydantic schemas
from app.auth import get_password_hash


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user."""
    vulnerabilities_json = json.dumps([
        v.value if hasattr(v, 'value') else v 
        for v in user_data.vulnerabilities
    ])
    
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        age=user_data.age,
        gender=user_data.gender.value if hasattr(user_data.gender, 'value') else user_data.gender,
        city=user_data.city.lower(),
        vulnerabilities=vulnerabilities_json
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "vulnerabilities" and value is not None:
            setattr(user, key, json.dumps([
                v.value if hasattr(v, 'value') else v for v in value
            ]))
        elif value is not None:
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True