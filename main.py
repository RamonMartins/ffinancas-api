from fastapi import FastAPI
from routers import lancamentos
from settings import settings

app = FastAPI(title="Ferreira Finanças API")


@app.get("/")
def root():
    return "Bem vindo ao Ferreira Finanças!"


@app.get("/loca")
def root():
    if settings.ENVIRONMENT == "development":
        return "Local atual é development"
    elif settings.ENVIRONMENT == "production":
        return "Local atual é production"
    else:
        return "Nenhum local identificado"


app.include_router(lancamentos.roteador)