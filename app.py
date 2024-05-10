# app.py

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy_operations import User, get_db, create_user, retrieve_user_name_by_id, update_user_name_by_id, search_users_by_name_cached
from face_recognition import process_uploaded_image
from functools import lru_cache  
from fastapi.responses import Response

app = FastAPI()

SECRET_KEY = "mysecretkey"
API_KEY_HEADER = APIKeyHeader(name="Authorization")

# Authorization function
def authorize(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# CRUD Operations
@app.post("/users/", response_model=None)
def create_user_handler(name: str, db: Session = Depends(get_db), authorized: bool = Depends(authorize)):
    return create_user(name, db)

@app.get("/users/{user_id}/name/", response_model=str)
def retrieve_user_name_by_id_handler(user_id: int, db: Session = Depends(get_db), authorized: bool = Depends(authorize)):
    return retrieve_user_name_by_id(user_id, db)

@app.put("/users/{user_id}/name/", response_model=None)
def update_user_name_by_id_handler(user_id: int, new_name: str, db: Session = Depends(get_db), authorized: bool = Depends(authorize)):
    return update_user_name_by_id(user_id, new_name, db)

# Search Functionality
@app.get("/users/search/", response_model=List[str])
def search_users_by_name_handler(name: str, db: Session = Depends(get_db), authorized: bool = Depends(authorize)):
    return search_users_by_name_cached(name, db)

# Image Processing Endpoint
@app.post("/process-image/")
async def process_uploaded_image_handler(file: UploadFile = File(...)):
    response,isFace = await process_uploaded_image(file)
    if isFace:
        return Response(response,media_type="image/png")
    else:
        return Response(response)
