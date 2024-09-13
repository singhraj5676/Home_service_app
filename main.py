# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import POSTGRES_API
from config import DATABASE_CONFIG
from routers import auth_routes, user_routes , get_routes, customer_routes, review_routes, favour_routes



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def startup():  
    db = POSTGRES_API(**DATABASE_CONFIG)
    print('creating')
    db.create_tables()

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
app.include_router(get_routes.router, prefix="/get_routes")
app.include_router(customer_routes.router, prefix="/customers")
app.include_router(review_routes.router, prefix="/review")
app.include_router(favour_routes.router, prefix="/favorite")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
