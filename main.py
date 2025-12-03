from fastapi import FastAPI
from routers import lancamentos
from .settings import settings

projeto = FastAPI(title="Ferreira Finanças API")


@projeto.get("/")
def root():
    return "Bem vindo ao Ferreira Finanças!"


@projeto.get("/loca")
def root():
    if settings.ENVIRONMENT == "development":
        return "Local atual é development"
    elif settings.ENVIRONMENT == "production":
        return "Local atual é production"
    else:
        return "Nenhum local identificado"


projeto.include_router(lancamentos.roteador)