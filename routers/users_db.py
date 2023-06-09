from fastapi import HTTPException, APIRouter, status

from database.models.user_models import User
from database.schemas.user import user_schema, users_schema
from database.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/userdb", 
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "No encontrado"}})






@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")
async def user1(id: str):
    return search_user('_id', ObjectId(id))
    

@router.get("/") 
async def user2(id: str):
    return search_user('_id', ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user('email', user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"] # no queremos que el id se guarde en la base de datos. Solo interesa que se 
    # guarde username y email; el id se encarga de generarlo MongoDB. 

    id = db_client.users.insert_one(user_dict).inserted_id # una vez que hemos insertado el usuario, 
    # ya podemos acceder al id generado por MongoDB.
    
    new_user = user_schema(db_client.users.find_one({"_id": id}))  # MongoDB no crea una clave llamada id, 
    # sino _id.
    return User(**new_user)

@router.put("/", response_model=User)
async def user3(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace({'_id': ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha encontrado el usuario a actualizar"}
    
    return search_user("_id", ObjectId(user.id))
        
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    Found = db_client.users.find_one_and_delete({'_id': ObjectId(id)})
    
    if not Found:
        return {"error":"No se ha eliminado el usuario"}

def search_user(field: str, key):
    
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}

