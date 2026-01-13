# app/utils/text_validator.py

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from fastapi import HTTPException

async def verificar_duplicidade(
    db: AsyncSession,
    model,
    campo: str,
    valor: str,
    mensagem_erro: str,
    cur_user: object | None = None,      # Usuário atual é opcional
    id_ignorar: UUID | None = None
):

    column_attr = getattr(model, campo)

    # Verifica qual banco esta sendo usado
    engine_name = db.bind.dialect.name

    if engine_name == "postgresql":
        # No postgresql podemos usar unaccent pois ele tem suporte
        filtro_texto = func.unaccent(func.lower(column_attr)) == func.unaccent(func.lower(valor))
    else:
        # No SQLite não tem suporte a unaccent
        filtro_texto = func.lower(column_attr) == func.lower(valor)

    # Monta a query inicial
    query = select(model).where(filtro_texto)

    # Caso tenha enviado o user na chamada, verifica se são do mesmo grupo familiar
    if cur_user and hasattr(cur_user, "grupo_familiar_id") and hasattr(model, "grupo_familiar_id"):
        if cur_user.grupo_familiar_id:
            query = query.where(model.grupo_familiar_id == cur_user.grupo_familiar_id)
    
    # No caso de uma rota de update, ignora o próprio objeto na busca
    if id_ignorar:
        query = query.where(model.id != id_ignorar)

    resultado = await db.execute(query)

    if resultado.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=mensagem_erro)
