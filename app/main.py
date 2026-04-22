from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.mobile_router import router
from app.db.database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "FastAPI LIVE 🚀"}