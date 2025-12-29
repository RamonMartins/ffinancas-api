# app/utils/text_validator.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from fastapi import HTTPException

async def verificar_duplicidade(db: AsyncSession, model, campo: str, valor: str, mensagem_erro: str):
    column_attr = getattr(model, campo)

    # Verifica qual banco esta sendo usado
    engine_name = db.bind.dialect.name

    if engine_name == "postgresql":
        # No postgresql podemos usar unaccent pois ele tem suporte
        filtro = func.unaccent(func.lower(column_attr)) == func.unaccent(func.lower(valor))
    else:
        # No SQLite não tem suporte a unaccent
        filtro = func.lower(column_attr) == func.lower(valor)

    query = select(model).where(filtro)

    resultado = await db.execute(query)

    if resultado.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=mensagem_erro)
