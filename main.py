from fastapi import FastAPI
from database.database import engine
from database import models
from routers import lancamentos
from settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ferreira Finanças API")


@app.get("/")
def root():
    return "Bem vindo ao Ferreira Finanças!"


@app.get("/local")
def local():
    if settings.ENVIRONMENT == "development":
        return {"message": "Local atual é development"}
    elif settings.ENVIRONMENT == "production":
        return {"message": "Local atual é production"}
    else:
        return {"message": "Nenhum local identificado"}

app.include_router(lancamentos.roteador)