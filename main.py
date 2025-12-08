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



app.include_router(lancamentos.roteador)