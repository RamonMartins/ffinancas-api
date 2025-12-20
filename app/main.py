# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.routers import lancamentos, carteiras
from app.core.config import settings
from fastapi.responses import ORJSONResponse

# Inicia a instância da API com title e ORJSON
app = FastAPI(title="Ferreira Finanças API", default_response_class=ORJSONResponse)
#app = FastAPI(title="Ferreira Finanças API")

"""
#Configuração do CORS
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
app.include_router(carteiras.roteador)