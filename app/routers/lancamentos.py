# app/routers/lancamentos.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.database.database import get_db
from app.database.models import LancamentoModel
from sqlalchemy.orm import Session
from app.schemas.lancamentos import *

roteador = APIRouter(prefix="/lancamentos", tags=["Lançamentos"])

#--------------------------
# GET - Todos os lançamentos
# Rota: GET "/lancamentos/list_all"
#--------------------------
@roteador.get("/list_all", response_model=list[LancamentoRead])
async def todos_lancamentos(db: Session = Depends(get_db)):
    lancamentos = db.query(LancamentoModel).all()
    return lancamentos


#--------------------------
# POST - Criar lançamento
# Rota: POST "/lancamentos/create/"
#--------------------------
# status_code é necessário para informar o resultado esperado da requisição
@roteador.post("/create", response_model=LancamentoCreate, status_code=201)
async def criar_lancamento(LancamentoSchema: LancamentoCreate, db: Session = Depends(get_db)):
    novo_lancamento = LancamentoModel(
        titulo= LancamentoSchema.titulo,
        is_active= LancamentoSchema.is_active
    )
    db.add(novo_lancamento)
    db.commit()
    # Refresh() é usado para atualizar o objeto do "novo_lancamento" com os dados mais recentes do banco de dados, incluindo o ID gerado automaticamente.
    # Caso nao queira retornar, deve remover essa linha, remover o response_model e ajustar o return.
    db.refresh(novo_lancamento)
    return novo_lancamento
    


"""#--------------------------
# POST - Criar novo lançamento
# Rota: POST "/lancamentos/"
#--------------------------
@roteador.post("/", response_model=LancamentoRead, status_code=201)
async def criar_lancamento(lancamento: LancamentoCreate, db: Session = Depends(get_db)):
    novo_lancamento = Lancamento(
        titulo=lancamento.titulo,
        is_active=lancamento.is_active
    )
    db.add(novo_lancamento)
    db.commit()
    db.refresh(novo_lancamento)
    return novo_lancamento


#--------------------------
# GET - Buscar lançamento por ID
# Rota: GET "/lancamentos/{id}"
#--------------------------
@roteador.get("/{id}", response_model=LancamentoRead)
async def obter_lancamento(id: int, db: Session = Depends(get_db)):
    lancamento = db.query(Lancamento).filter(Lancamento.id == id).first()
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    return lancamento


#--------------------------
# PUT - Atualizar lançamento
# Rota: PUT "/lancamentos/{id}"
#--------------------------
@roteador.put("/{id}", response_model=LancamentoRead)
async def atualizar_lancamento(id: int, lancamento: LancamentoUpdate, db: Session = Depends(get_db)):
    db_lancamento = db.query(Lancamento).filter(Lancamento.id == id).first()
    if not db_lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    
    db_lancamento.titulo = lancamento.titulo
    db_lancamento.is_active = lancamento.is_active
    
    db.commit()
    db.refresh(db_lancamento)
    return db_lancamento


#--------------------------
# DELETE - Deletar lançamento
# Rota: DELETE "/lancamentos/{id}"
#--------------------------
@roteador.delete("/{id}", status_code=204)
async def deletar_lancamento(id: int, db: Session = Depends(get_db)):
    lancamento = db.query(Lancamento).filter(Lancamento.id == id).first()
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    
    db.delete(lancamento)
    db.commit()
    return
"""