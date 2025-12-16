from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database import models
from routers import lancamentos
from settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ferreira Finanças API")

"""Configuração de CORS
if settings.ENVIRONMENT == "production":
    FRONT_URL_CORS = f"https://{settings.FRONT_URL}"
else:
    FRONT_URL_CORS = "http://localhost:3000"

origins = [
    FRONT_URL_CORS,
    #"https://ffinancas-web.up.railway.app",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

@app.get("/")
def root():
    return "Bem vindo ao Ferreira Finanças!"



app.include_router(lancamentos.roteador)