from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

def verificar_duplicidade(db: Session, model, campo: str, valor: str, mensagem_erro: str):
    column_attr = getattr(model, campo)

    # Verifica qual banco esta sendo usado
    engine_name = db.get_bind().dialect.name

    if engine_name == "postgresql":
        # No postgresql podemos usar unaccent pois ele tem suporte
        filtro = func.unaccent(func.lower(column_attr)) == func.unaccent(func.lower(valor))
    else:
        # No SQLite não tem suporte a unaccent
        filtro = func.lower(column_attr) == func.lower(valor)

    query = db.query(model).filter(filtro).first()

    if query:
        raise HTTPException(status_code=400, detail=mensagem_erro)