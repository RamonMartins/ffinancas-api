# app/database/models.py

import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.config import Brasil_TZ, settings
from datetime import datetime
from .database import Base

"""
Mapped[int]                 INTEGER             Números inteiros.
Mapped[str]                 VARCHAR ou TEXT     Textos e strings.
Mapped[float]	            FLOAT               Números decimais.
Mapped[bool]	            BOOLEAN             Verdadeiro ou Falso.
Mapped[bytes]	            BLOB ou BYTEA       Arquivos, imagens ou dados binários.
Mapped[datetime.datetime]   
Mapped[datetime.date]
Mapped[datetime.time]

Mapped[Optional[str]]               Campo opcional/Não obrigatório
"""

class CarteiraModel(Base):
    __tablename__ = "Carteiras"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default= uuid.uuid4)
    titulo: Mapped[str] = mapped_column(nullable=False)
    saldo: Mapped[float | None] = mapped_column(default=0.0)
    created_at_utc = Column(DateTime(timezone=True), default=lambda: datetime.now(Brasil_TZ))

    @property
    def created_at(self):
        return self.created_at_utc.astimezone(Brasil_TZ)


class UsuarioModel(Base):
    __tablename__ = "Usuarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default= uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    created_at_utc = Column(DateTime(timezone=True), default=lambda: datetime.now(Brasil_TZ))

    @property
    def created_at(self):
        return self.created_at_utc.astimezone(Brasil_TZ)


class LancamentoModel(Base):
    __tablename__ = "Lancamentos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default= uuid.uuid4)
    titulo = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at_utc = Column(DateTime(timezone=True), default=lambda: datetime.now(Brasil_TZ))

    @property
    def created_at(self):
        return self.created_at_utc.astimezone(Brasil_TZ)
