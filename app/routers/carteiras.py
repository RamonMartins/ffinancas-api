# app/routers/carteiras.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.database.session import get_db
from app.database.models import CarteiraModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.schemas.carteiras import *
from app.utils.text_validator import verificar_duplicidade
from sqlalchemy import select
from app.database.models import UsuarioModel
from app.core.auth import current_user, current_user_superuser


roteador = APIRouter(prefix="/carteiras", tags=["Carteiras"])

#--------------------------
# GET - Todas as Carteiras - SUPERUSER
# Rota: GET "/carteiras/admin"
#--------------------------
@roteador.get("/admin", response_model=list[CarteiraRead])
async def todas_carteiras_superuser(
    db: AsyncSession = Depends(get_db),
    admin: UsuarioModel = Depends(current_user_superuser)
):
    
    # Escreve a consulta(execute()), envia ao banco e aguarda a resposta(await).
    carteiras = await db.execute(select(CarteiraModel))
    # Faz a extração do resultado para objetos, como é lista usa scalars no plural.
    return carteiras.scalars().all()


#--------------------------
# GET - Todas as Carteiras do usuário atual
# Rota: GET "/carteiras"
#--------------------------
@roteador.get("", response_model=list[CarteiraRead])
async def todas_carteiras(
    db: AsyncSession = Depends(get_db),
    user: UsuarioModel = Depends(current_user)
):
    
    # Escreve a consulta(execute()), envia ao banco e aguarda a resposta(await).
    carteiras = await db.execute(
        select(CarteiraModel)
        .where(CarteiraModel.grupo_familiar_id == user.grupo_familiar_id)
    )
    # Faz a extração do resultado para objetos, como é lista usa scalars no plural.
    return carteiras.scalars().all()


#--------------------------
# POST - Criar Carteira - SUPERUSER
# Rota: POST "/carteiras/admin"
#--------------------------
# status_code é necessário para informar o resultado esperado da requisição
@roteador.post("/admin", response_model=CarteiraRead, status_code=201)
async def criar_carteira_superuser(
    payload: CarteiraCreate,
    db: AsyncSession = Depends(get_db),
    admin: UsuarioModel = Depends(current_user_superuser)
):
    
    # Verifica se tem duplicidade no banco de dados
    await verificar_duplicidade(
        db,
        model=CarteiraModel,
        campo="titulo",
        valor=payload.titulo,
        mensagem_erro=f"Já existe uma Carteira criada com o título '{payload.titulo}'"
    )

    # O model_dump pega o objeto payload com as propriedades e desempacota em formato JSON
    # Os asteriscos (**) serve para entregar ao constructor CarteiraModel as propriedades uma a uma
    nova_carteira = CarteiraModel(**payload.model_dump())
    db.add(nova_carteira)
    await db.commit()
    # Refresh() é usado para atualizar o objeto do "novo_lancamento" com os dados mais recentes do banco de dados, incluindo o ID gerado automaticamente.
    # Caso nao queira retornar, deve remover essa linha, remover o response_model e ajustar o return.
    await db.refresh(nova_carteira)
    return nova_carteira


#--------------------------
# POST - Criar Carteira para usuário atual
# Rota: POST "/carteiras"
#--------------------------
# status_code é necessário para informar o resultado esperado da requisição
@roteador.post("", response_model=CarteiraRead, status_code=201)
async def criar_carteira(
    payload: CarteiraCreate,
    db: AsyncSession = Depends(get_db),
    user: UsuarioModel = Depends(current_user)
):
    # Pega os dados do payload
    dados = payload.model_dump()
    # Insere o ID do Grupo Familiar do usuário Logado
    dados["grupo_familiar_id"] = user.grupo_familiar_id
    
    # Verifica se tem duplicidade no banco de dados
    await verificar_duplicidade(
        db,
        model=CarteiraModel,
        campo="titulo",
        valor=payload.titulo,
        mensagem_erro=f"Já existe uma Carteira criada com o título '{payload.titulo}'",
        cur_user=user
    )

    # O model_dump pega o objeto payload com as propriedades e desempacota em formato JSON
    # Os asteriscos (**) serve para entregar ao constructor CarteiraModel as propriedades uma a uma
    nova_carteira = CarteiraModel(**dados)
    db.add(nova_carteira)
    await db.commit()
    # Refresh() é usado para atualizar o objeto do "novo_lancamento" com os dados mais recentes do banco de dados, incluindo o ID gerado automaticamente.
    # Caso nao queira retornar, deve remover essa linha, remover o response_model e ajustar o return.
    await db.refresh(nova_carteira)
    return nova_carteira


#--------------------------
# PATCH - Atualizar Carteira - SUPERUSER
# Rota: PATCH "/carteiras/admin/[id]"
#--------------------------
@roteador.patch("/admin/{carteira_id}", response_model=CarteiraRead)
async def editar_carteira_superuser(
    carteira_id: UUID,
    payload: CarteiraUpdate,
    db: AsyncSession = Depends(get_db),
    admin: UsuarioModel = Depends(current_user_superuser)
):
    # Busca o objeto no Banco pesquisando pelo id passado
    obj_alvo = await db.get(CarteiraModel, carteira_id)

    # Trata o erro caso não encontre o objeto
    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    
    # Valida duplicidade, ignorando o objeto atual
    if payload.titulo:
        await verificar_duplicidade(
            db,
            model=CarteiraModel,
            campo="titulo",
            valor=payload.titulo,
            mensagem_erro=f"Já existe uma Carteira criada com o título '{payload.titulo}'",
            id_ignorar=carteira_id
        )
    
    # O model_dump desmonta o objeto em JSON
    # O CarteiraUpdate monta um Dic com a propriedades definidas, se usuario mandar apenas uma o exclude_unset remove a outra
    novos_dados = payload.model_dump(exclude_unset=True)

    # Variavel campo e valor recebem respectivamente do Dic enviado pelo usuario
    # setattr pega o objeto do banco e altera o valor com base na propriedade
    for campo, valor in novos_dados.items():
        setattr(obj_alvo, campo, valor)
    
    db.add(obj_alvo)
    await db.commit()
    await db.refresh(obj_alvo)
    return obj_alvo


#--------------------------
# PATCH - Atualizar Carteira do usuário atual
# Rota: PATCH "/carteiras/[id]"
#--------------------------
@roteador.patch("/{carteira_id}", response_model=CarteiraRead)
async def editar_carteira(
    carteira_id: UUID,
    payload: CarteiraUpdate,
    db: AsyncSession = Depends(get_db),
    user: UsuarioModel = Depends(current_user)
):
    # Busca o objeto no Banco pesquisando pelo id passado
    obj_alvo = await db.get(CarteiraModel, carteira_id)

    # Trata o erro caso não encontre o objeto
    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    
    if obj_alvo.grupo_familiar_id != user.grupo_familiar_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para editar esta carteira")
    
    # Valida duplicidade, ignorando o objeto atual
    if payload.titulo:
        await verificar_duplicidade(
            db,
            model=CarteiraModel,
            campo="titulo",
            valor=payload.titulo,
            mensagem_erro=f"Já existe uma Carteira criada com o título '{payload.titulo}'",
            cur_user=user,
            id_ignorar=carteira_id
        )
    
    # O model_dump desmonta o objeto em JSON
    # O CarteiraUpdate monta um Dic com a propriedades definidas, se usuario mandar apenas uma o exclude_unset remove a outra
    novos_dados = payload.model_dump(exclude_unset=True)

    # Variavel campo e valor recebem respectivamente do Dic enviado pelo usuario
    # setattr pega o objeto do banco e altera o valor com base na propriedade
    for campo, valor in novos_dados.items():
        setattr(obj_alvo, campo, valor)
    
    db.add(obj_alvo)
    await db.commit()
    await db.refresh(obj_alvo)
    return obj_alvo


#--------------------------
# DELETE - Remover Carteira - SUPERUSER
# Rota: DELETE "/carteiras/admin/[id]"
#--------------------------
@roteador.delete("/admin/{carteira_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_carteira_superuser(
    carteira_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin: UsuarioModel = Depends(current_user_superuser)
):

    obj_alvo = await db.get(CarteiraModel, carteira_id)

    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")

    await db.delete(obj_alvo)
    await db.commit()
    return None


#--------------------------
# DELETE - Remover Carteira do usuário atual
# Rota: DELETE "/carteiras/[id]"
#--------------------------
@roteador.delete("/{carteira_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_carteira(
    carteira_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: UsuarioModel = Depends(current_user)
):

    obj_alvo = await db.get(CarteiraModel, carteira_id)

    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    
    if obj_alvo.grupo_familiar_id != user.grupo_familiar_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para excluir esta carteira")

    await db.delete(obj_alvo)
    await db.commit()
    return None