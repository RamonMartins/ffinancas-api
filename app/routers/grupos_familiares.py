# app/routers/grupos_familiares.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.database.session import get_db
from app.database.models import GrupoFamiliarModel, UsuarioModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.grupos_familiares import *
from app.utils.text_validator import verificar_duplicidade
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.auth import current_user


roteador = APIRouter(prefix="/grupos-familiares", tags=["Grupos Familiares"])

#--------------------------
# GET - Todos os Grupos Familiares
# Rota: GET "/grupos-familiares"
#--------------------------
@roteador.get("", response_model=list[GrupoFamiliarRead])
async def todos_grupos(db: AsyncSession = Depends(get_db)):

    stmt = select(GrupoFamiliarModel)
    grupos = await db.execute(stmt)
    return grupos.scalars().all()


#--------------------------
# POST - Cria Grupo Familiar e associa ao usuário atual
# Rota: POST "/grupos-familiares"
#--------------------------
@roteador.post("", response_model=GrupoFamiliarRead, status_code=201)
async def criar_vincular_grupo(
    payload: GrupoFamiliarCreate,
    db: AsyncSession = Depends(get_db),
    user: UsuarioModel = Depends(current_user)
):
    
    if user.lider_familiar is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Líderes Familiares podem criar Grupos Familiares."
        )

    if user.grupo_id is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário já pertence a um Grupo Familiar e não pode criar outro."
        )

    await verificar_duplicidade(
        db,
        model=GrupoFamiliarModel,
        campo="titulo",
        valor=payload.titulo,
        mensagem_erro=f"Já existe um Grupo familiar com o título '{payload.titulo}'"
    )

    novo_grupo = GrupoFamiliarModel(**payload.model_dump())
    db.add(novo_grupo)

    # Gera o ID do novo grupo mas não grava no banco ainda
    await db.flush()

    # Associa o usuário atual ao novo grupo
    user.grupo_id = novo_grupo.id
    
    await db.commit()
    stmt = (
        select(GrupoFamiliarModel)
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


#--------------------------
# DELETE - Remover Grupo Familiar
# Rota: DELETE "/grupos-familiares/[id]"
#--------------------------
@roteador.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_grupo(grupo_id: UUID, db: AsyncSession = Depends(get_db)):

    obj_alvo = await db.get(GrupoFamiliarModel, grupo_id)

    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Grupo Familiar não encontrada")

    await db.delete(obj_alvo)
    await db.commit()
    return None