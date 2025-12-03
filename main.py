from fastapi import FastAPI
from routers import lancamentos

projeto = FastAPI(title="Ferreira Finanças API")


@projeto.get("/")
def root():
    return "Bem vindo ao Ferreira Finanças!"


projeto.include_router(lancamentos.roteador)