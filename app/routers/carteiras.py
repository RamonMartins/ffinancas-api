# app/routers/carteiras.py

from fastapi import APIRouter, HTTPException, status, Depends
from app.database.session import get_db
from app.database.models import CarteiraModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.schemas.carteiras import *
from app.utils.text_validator import verificar_duplicidade
from sqlalchemy import select


roteador = APIRouter(prefix="/carteiras", tags=["Carteiras"])

#--------------------------
# GET - Todas as Carteiras
# Rota: GET "/carteiras"
#--------------------------
@roteador.get("", response_model=list[CarteiraRead])
async def todas_carteiras(db: AsyncSession = Depends(get_db)):
    
    # Escreve a consulta(execute()), envia ao banco e aguarda a resposta(await).
    carteiras = await db.execute(select(CarteiraModel))
    # Faz a extração do resultado para objetos, como é lista usa scalars no plural.
    return carteiras.scalars().all()


#--------------------------
# POST - Criar Carteira
# Rota: POST "/carteiras"
#--------------------------
# status_code é necessário para informar o resultado esperado da requisição
@roteador.post("", response_model=CarteiraRead, status_code=201)
async def criar_carteira(payload: CarteiraCreate, db: AsyncSession = Depends(get_db)):
    
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
# PATCH - Atualizar Carteira
# Rota: PATCH "/carteiras/[id]"
#--------------------------
@roteador.patch("/{carteira_id}", response_model=CarteiraRead)
async def editar_carteira(carteira_id: UUID, payload: CarteiraUpdate, db: AsyncSession = Depends(get_db)):
    # Busca o objeto no Banco pesquisando pelo id passado
    obj_alvo = await db.get(CarteiraModel, carteira_id)

    # Trata o erro caso não encontre o objeto
    if not obj_alvo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    
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
