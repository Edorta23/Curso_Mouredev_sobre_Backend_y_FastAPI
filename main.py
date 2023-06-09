from fastapi import FastAPI, Cookie, Header
from routers import products, users, basic_auth_users, jwt_auth_users, users_db # nos da acceso al  fichero products.py y users.py
from fastapi.staticfiles import StaticFiles


app = FastAPI()

@app.get("/cookies") # http://localhost:8000/cookies?ads_id=1234
async def cookies(ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}

@app.get("/headers") # http://localhost:8000/headers?user_agent=Mozilla
async def headers(user_agent: str = Header(None)):
    return {"user_agent": user_agent}

#routers
app.include_router(products.router) 
app.include_router(users.router) 
app.include_router(basic_auth_users.router) 
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return "Hola Mundo"

@app.get("/url")
async def url():
    return {"url_curso":"https://mouredev.com/python"}
