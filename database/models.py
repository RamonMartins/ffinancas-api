from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from settings import Brasil_TZ
from datetime import datetime
from .database import Base


class UsuarioModel(Base):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    nome = Column(String, nullable=False)


class LancamentoModel(Base):
    __tablename__ = "Lancamentos"

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    # TODO: Ajustar fuso horário definindo ele diretamente no banco de dados e usar o código abaixo:
    #created_at = Column(DateTime, default=func.now())

    # lambda garante que a data seja gerada na hora da criação do objeto
    created_at = Column(DateTime, default=lambda: datetime.now(Brasil_TZ))