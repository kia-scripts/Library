from fastapi import FastAPI
from routes.library import library_route
from routes.auth import auth_route

app = FastAPI()

app.include_router(library_route)
app.include_router(auth_route)
