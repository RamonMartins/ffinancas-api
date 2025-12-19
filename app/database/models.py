# app/database/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from app.core.config import Brasil_TZ, settings
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
    created_at_utc = Column(DateTime(timezone=True), default=lambda: datetime.now(Brasil_TZ))

    @property
    def created_at(self):
        return self.created_at_utc.astimezone(Brasil_TZ)
