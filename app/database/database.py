# app/database/database.py

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Coleta a URL do banco a depender do ambiente
BD_URL = settings.DATABASE_URL

# create_engine é o motor que a biblioteca SQLAlchemy usa para se comunicar com o banco de dados.
# connect_args é necessário apenas para SQLite.
if settings.ENVIRONMENT == "development":
    engine = create_engine(BD_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(BD_URL)

# SessionLocal será a classe de sessão real do banco de dados.
# Cada instância de SessionLocal será uma sessão de banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe base para criar os modelos de banco de dados (tabelas).
Base = declarative_base()

# Função que será usada como uma 'Dependência' no FastAPI
def get_db():
    db = SessionLocal() # Abre a sessão
    try:
        yield db        # Retorna a sessão ao endpoint
    finally:
        db.close()      # Garante que a sessão seja fechada, mesmo em caso de erro