# app/routers/carteiras.py

from fastapi import APIRouter, Depends
from app.database.database import get_db
from app.database.models import CarteiraModel
from sqlalchemy.orm import Session
from app.schemas.carteiras import *

roteador = APIRouter(prefix="/carteiras", tags=["Carteiras"])

#--------------------------
# GET - Todas as Carteiras
# Rota: GET "/carteiras/list_all"
#--------------------------
@roteador.get("/list_all", response_model=list[CarteiraRead])
async def todas_carteiras(db: Session = Depends(get_db)):
    carteiras = db.query(CarteiraModel).all()
    return carteiras


#--------------------------
# POST - Criar Carteira
# Rota: POST "/carteiras/create/"
#--------------------------
# status_code é necessário para informar o resultado esperado da requisição
@roteador.post("/create", response_model=CarteiraCreate, status_code=201)
async def criar_carteira(CarteiraSchema: CarteiraCreate, db: Session = Depends(get_db)):
    nova_carteira = CarteiraModel(
        titulo = CarteiraSchema.titulo,
        saldo = CarteiraSchema.saldo
    )
    db.add(nova_carteira)
    db.commit()
    # Refresh() é usado para atualizar o objeto do "novo_lancamento" com os dados mais recentes do banco de dados, incluindo o ID gerado automaticamente.
    # Caso nao queira retornar, deve remover essa linha, remover o response_model e ajustar o return.
    db.refresh(nova_carteira)
    return nova_carteira