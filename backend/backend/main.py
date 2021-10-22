from datetime import datetime
from typing import Optional
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    password: Optional[str] = None
    data_de_nascimento: Optional[datetime]
    sexo: Optional[str]

class LoginModel(BaseModel):
    email: str
    password: str

class NotFoundError(BaseModel):
    message: str


users = [
    User(name='Homer Simpson', email='homer.simpson@email.com'),
    User(name='Bart Simpson', email='bart.simpson@email.com'),
    User(name='Marge Simpson', email='marge.simpson@email.com'),
    User(name='Lisa Simpson', email='lisa.simpson@email.com')
]

@app.get("/hello")
def hello():
    return {"message": "hello, world"}




@app.post("/login")
def login(user: LoginModel):    
    return {"user": user}





@app.get("/users")
def list_all():
    """Endpoint to return all users

    Returns:
        users: A list of users
    """
    return users


@app.get("/users/{user_id}", responses = {404: {"model": NotFoundError}})
def read_item(user_id: int, q: Optional[str] = None):
    if user_id < len(users):
        return {"user": users[user_id]}
    
    return JSONResponse(status_code=404, content={"message": "Usuário não encontrado"})


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create(user: User):
    users.append(user)
    return {"user": user}





@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: User):
    users.append(user)
    return {"user": user}
