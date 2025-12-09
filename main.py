from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database import models
from routers import lancamentos
from settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ferreira Finanças API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    settings.FRONT_URL,
    # E o seu domínio de produção, que discutimos anteriormente
    # "https://seu-front-end-railway.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return "Bem vindo ao Ferreira Finanças!"



app.include_router(lancamentos.roteador)