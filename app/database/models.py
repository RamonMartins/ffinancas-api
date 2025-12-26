# app/database/models.py

import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.config import Brasil_TZ, settings
from datetime import datetime
from .database import Base

"""
> Type Hints

Mapped[int]                 INTEGER             Números inteiros.
Mapped[str]                 VARCHAR ou TEXT     Textos e strings.
Mapped[float]	            FLOAT               Números decimais.
Mapped[bool]	            BOOLEAN             Verdadeiro ou Falso.
Mapped[bytes]	            BLOB ou BYTEA       Arquivos, imagens ou dados binários.
Mapped[datetime]   

Mapped[Optional[str]]               Campo opcional/Não obrigatório
"""

class CarteiraModel(Base):
    __tablename__ = "carteiras"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo: Mapped[str] = mapped_column(nullable=False)
    # Usar o operador '| None' é melhor do que usar 'Optional[str]' pois não precisa importar dependência.
    saldo: Mapped[float | None] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(Brasil_TZ))

    @property
    def created_at(self):
        return self.created_at_utc.astimezone(Brasil_TZ)


class LancamentoModel(Base):
    __tablename__ = "lancamentos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(Brasil_TZ))

    @property
    def created_at(self):
        return self.created_at_utc.astimezone(Brasil_TZ)
