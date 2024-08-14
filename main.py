# main.py

from fastapi import FastAPI
from routers.main_router import router
from config import DATABASE_CONFIG
from database import POSTGRES_API
from routers import auth_routes, user_routes , get_routes



app = FastAPI()

@app.on_event("startup")
def startup():
    db = POSTGRES_API(**DATABASE_CONFIG)
    print('creating')
    db.create_tables()

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
app.include_router(get_routes.router, prefix="/get_routes")
# app.include_router(user_routes.router, prefix="/users")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
