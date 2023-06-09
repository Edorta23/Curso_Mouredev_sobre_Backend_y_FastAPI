from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# BaseModel nos da ciertos mecanismos para que este objeto, que hemos definido como una clase,
# pueda ser tratado como un JSON y que pueda ser validado por FastAPI; es decir, que pueda pasar por
# la red de una manera muy fácil.

# Este usuario, User(BaseModel) ↓↓↓, es el que va a ir a través de la red y por ello no le creamos una contraseña.
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str
    




users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "johndoe2": {
        "username": "johndoe2",
        "full_name": "John Doe2",
        "email": "johndoe2@gmail.com",
        "disabled": True,
        "password": "1234567"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticación inválidas", 
                            headers={'www-Authenticate': 'Bearer'})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password: # comprobamos la contraseña con la contraseña del usuario de BD.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)): # devuelve usuario sin contraseña porque, de otra 
# forma, sería una brecha de seguridad enorme.
    # que esté autenticado.
    return user