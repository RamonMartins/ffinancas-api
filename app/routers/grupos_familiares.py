# app/routers/grupos_familiares.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.database.session import get_db
from app.database.models import GrupoFamiliarModel
from sqlalchemy.orm import Session
from app.schemas.grupos_familiares import *
from app.utils.text_validator import verificar_duplicidade


roteador = APIRouter(prefix="/grupos-familiares", tags=["Grupos Familiares"])

#--------------------------
# GET - Todos os Grupos Familiares
# Rota: GET "/grupos-familiares"
#--------------------------
@roteador.get("", response_model=list[GrupoFamiliarRead])
def todos_grupos(db: Session = Depends(get_db)):
    
    grupos = db.query(GrupoFamiliarModel).all()
    return grupos


#--------------------------
# POST - Criar Grupo Familiar
# Rota: POST "/grupos-familiares"
#--------------------------
@roteador.post("", response_model=GrupoFamiliarRead, status_code=201)
def criar_grupo(payload: GrupoFamiliarCreate, db: Session = Depends(get_db)):

    verificar_duplicidade(
        db,
        model=GrupoFamiliarModel,
        campo="titulo",
        valor=payload.titulo,
        mensagem_erro=f"Já existe um Grupo familiar com o título '{payload.titulo}'"
    )

    novo_grupo = GrupoFamiliarModel(**payload.model_dump())
    db.add(novo_grupo)
    db.commit()
    db.refresh(novo_grupo)
    return novo_grupo


#--------------------------
# PATCH - Atualizar Grupo Familiar
# Rota: PATCH "/grupos-familiares/[id]"
#--------------------------
@roteador.patch("/{grupo_id}", response_model=GrupoFamiliarRead)
def editar_grupo(grupo_id: UUID, payload: GrupoFamiliarUpdate, db: Session = Depends(get_db)):
    
    obj_alvo = db.get(GrupoFamiliarModel, grupo_id)

    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo Familiar não encontrado")
    
    novos_dados = payload.model_dump(exclude_unset=True)

    for campo, valor in novos_dados.items():
        setattr(obj_alvo, campo, valor)
    
    db.add(obj_alvo)
    db.commit()
    db.refresh(obj_alvo)
    return obj_alvo
