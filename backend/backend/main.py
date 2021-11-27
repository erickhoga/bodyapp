from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine



models.Base.metadata.create_all(bind=engine)
    
app = FastAPI()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = crud.create_user(db=db, user=user)
    
    return user

@app.post("/users/{item_id}/measures/", response_model=schemas.Measure)
def create_measure(item_id:int,measure: schemas.UserCreate, db: Session = Depends(get_db)):

    measure = crud.create_user_measure(db=db, measure=measure, user_id=item_id)
    
    return measure

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/measures/", response_model=List[schemas.Measure])
def read_measures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    measures = crud.get_measures(db, skip=skip, limit=limit)
    return measures


@app.get("/users/{item_id}", response_model=schemas.User)
def read_users(item_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=item_id)
    return user

