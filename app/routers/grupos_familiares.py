# app/routers/grupos_familiares.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.database.session import get_db
from app.database.models import GrupoFamiliarModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.grupos_familiares import *
from app.utils.text_validator import verificar_duplicidade
from sqlalchemy import select
from sqlalchemy.orm import selectinload


roteador = APIRouter(prefix="/grupos-familiares", tags=["Grupos Familiares"])

#--------------------------
# GET - Todos os Grupos Familiares
# Rota: GET "/grupos-familiares"
#--------------------------
@roteador.get("", response_model=list[GrupoFamiliarRead])
async def todos_grupos(db: AsyncSession = Depends(get_db)):

    stmt = select(GrupoFamiliarModel).options(selectinload(GrupoFamiliarModel.carteiras))
    grupos = await db.execute(stmt)
    return grupos.scalars().all()


#--------------------------
# POST - Criar Grupo Familiar
# Rota: POST "/grupos-familiares"
#--------------------------
@roteador.post("", response_model=GrupoFamiliarRead, status_code=201)
async def criar_grupo(payload: GrupoFamiliarCreate, db: AsyncSession = Depends(get_db)):

    await verificar_duplicidade(
        db,
        model=GrupoFamiliarModel,
        campo="titulo",
        valor=payload.titulo,
        mensagem_erro=f"Já existe um Grupo familiar com o título '{payload.titulo}'"
    )

    novo_grupo = GrupoFamiliarModel(**payload.model_dump())
    db.add(novo_grupo)
    await db.commit()
    stmt = (
        select(GrupoFamiliarModel)
        .options(selectinload(GrupoFamiliarModel.carteiras))
        .where(GrupoFamiliarModel.id == novo_grupo.id)
    )
    resultado = await db.execute(stmt)
    return resultado.scalar_one()


#--------------------------
# PATCH - Atualizar Grupo Familiar
# Rota: PATCH "/grupos-familiares/[id]"
#-------------------------- 
@roteador.patch("/{grupo_id}", response_model=GrupoFamiliarRead)
async def editar_grupo(grupo_id: UUID, payload: GrupoFamiliarUpdate, db: AsyncSession = Depends(get_db)):
    
    stmt_busca = (
        select(GrupoFamiliarModel)
        .options(selectinload(GrupoFamiliarModel.carteiras))
        .where(GrupoFamiliarModel.id == grupo_id)
    )
    resultado_busca = await db.execute(stmt_busca)
    obj_alvo = resultado_busca.scalar_one_or_none()

    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo Familiar não encontrado")
    
    novos_dados = payload.model_dump(exclude_unset=True)

    for campo, valor in novos_dados.items():
        setattr(obj_alvo, campo, valor)
    
    db.add(obj_alvo)
    await db.commit()
    await db.refresh(obj_alvo)
    return obj_alvo
