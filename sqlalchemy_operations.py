from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from functools import lru_cache
from fastapi import FastAPI, HTTPException


SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(name: str, db):
    user = User(name=name)
    db.add(user)
    db.commit()
    return "User Added!"

def retrieve_user_name_by_id(user_id: int, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return f"ID: {user.id} Name: {user.name}"

def update_user_name_by_id(user_id: int, new_name: str, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = new_name
    db.commit()
    return f"User Name Updated to {user.name} at ID {user.id}"

@lru_cache(maxsize=128)
def search_users_by_name_cached(name: str, db):
    users = db.query(User).filter(User.name.like(f'%{name}%')).all()
    return [user.name for user in users]
