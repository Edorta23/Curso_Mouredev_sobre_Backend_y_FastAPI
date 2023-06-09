from fastapi import HTTPException, APIRouter
from pydantic import BaseModel


router = APIRouter()

# inicia el servidor con uvicorn users:app --reload

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


# Objeto ↓↓↓ que implementa el comportamiento de BaseModel y que podemos manejar como un JSON
users_list = [User(id=1, name="John", surname="lightyear", url="light.years", age=25),
              User(id=2, name="Jane", surname="killer", url="killer.jane", age=30),
              User(id=3, name="Joe", surname="Doe", url="joe.doe", age=20)] 


#Ejemplo de como devolver un JSON pero creando cada usuario manualmente con la estructura par clave/valor
@router.get("/usersJSON")
async def usersJSON():
    return [{"name": "John", "surname": "lightyear", "url": "light.years", "age": 25},
            {"name": "Jane", "surname": "killer", "url": "killer.jane", "age": 30}, 
            {"name": "Joe", "surname": "Doe", "url": "joe.doe", "age": 20}] # → JSON



#Path
@router.get("/users")
async def users():
    return users_list

#Path. Funciona con la llamada mediante el path (user/1, user/2, etc)
@router.get("/user/{id}")
async def user1(id: int):
    return search_user(id)
    
#Query. Funciona con la llamada mediante el query (user/?id=)
@router.get("/user/") 
async def user2(id: int):
    return search_user(id)


@router.post("/user", response_model=User, status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    else:
        users_list.append(user)


@router.put("/user")
async def user3(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"No se ha encontrado el usuario a actualizar"}
    
@router.delete("/user/{id}")
async def user(id: int):
    Found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            Found = True
    if not Found:
        return {"error":"No se ha eliminado el usuario"}

def search_user(id):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0] # el objeto filter hay que devolverlo como una lista
    except:
        return {"error": "user not found"}