# app/routers/lancamentos.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.database.session import get_db
from app.database.models import LancamentoModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.lancamentos import *
from app.utils.text_validator import verificar_duplicidade
from sqlalchemy import select


roteador = APIRouter(prefix="/lancamentos", tags=["Lançamentos"])

#--------------------------
# GET - Todos os lançamentos
# Rota: GET "/lancamentos"
#--------------------------
@roteador.get("", response_model=list[LancamentoRead])
async def todos_lancamentos(db: AsyncSession = Depends(get_db)):

    grupos = await db.execute(select(LancamentoModel))
    return grupos.scalars().all()


#--------------------------
# POST - Criar lançamento
# Rota: POST "/lancamentos"
#--------------------------
# status_code é necessário para informar o resultado esperado da requisição
@roteador.post("", response_model=LancamentoRead, status_code=201)
async def criar_lancamento(payload: LancamentoCreate, db: AsyncSession = Depends(get_db)):

    # Verifica se tem duplicidade no banco de dados
    await verificar_duplicidade(
        db,
        model=LancamentoModel,
        campo="titulo",
        valor=payload.titulo,
        mensagem_erro=f"Já existe um Lançamento criado com o título '{payload.titulo}'"
    )

    # O model_dump pega o objeto payload com as propriedades e desempacota em formato JSON
    # Os asteriscos (**) serve para entregar ao constructor LancamentoModel as propriedades uma a uma
    novo_lancamento = LancamentoModel(**payload.model_dump())
    db.add(novo_lancamento)
    await db.commit()
    # Refresh() é usado para atualizar o objeto do "novo_lancamento" com os dados mais recentes do banco de dados, incluindo o ID gerado automaticamente.
    # Caso nao queira retornar, deve remover essa linha, remover o response_model e ajustar o return.
    await db.refresh(novo_lancamento)
    return novo_lancamento
    

#--------------------------
# PATCH - Atualizar Lançamento
# Rota: PATCH "/lancamentos/[id]"
#--------------------------
@roteador.patch("/{lancamento_id}", response_model=LancamentoRead)
async def editar_lancamento(lancamento_id: UUID, payload: LancamentoUpdate, db: AsyncSession = Depends(get_db)):

    obj_alvo = await db.get(LancamentoModel, lancamento_id)

    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lançamento não encontrado")
    
    novos_dados = payload.model_dump(exclude_unset=True)

    for campo, valor in novos_dados.items():
        setattr(obj_alvo, campo, valor)
    
    db.add(obj_alvo)
    await db.commit()
    await db.refresh(obj_alvo)
    return obj_alvo


#--------------------------
# DELETE - Remover Lançamento
# Rota: DELETE "/lancamentos/[id]"
#--------------------------
@roteador.delete("/{lancamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_lancamento(lancamento_id: UUID, db: AsyncSession = Depends(get_db)):

    obj_alvo = await db.get(LancamentoModel, lancamento_id)

    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Lançamento não encontrada")

    await db.delete(obj_alvo)
    await db.commit()
    return None