from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr, BaseModel


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
    
conf = ConnectionConfig(
    MAIL_USERNAME = "YourUsername",
    MAIL_PASSWORD = "strong_password",
    MAIL_FROM = "mario.adaniya@email.com",
    MAIL_PORT = 1025,
    MAIL_SERVER = "mailhog",
    MAIL_TLS = False,
    MAIL_SSL = False,
    USE_CREDENTIALS = False,
    VALIDATE_CERTS = False
)

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
    
    html = """
    <p>Thanks for using Fastapi-mail</p> 
    """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[user.email], 
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    fm.send_message(message)
    
    return user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users