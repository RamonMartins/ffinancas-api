# app/database/models.py

import uuid
from sqlalchemy import ForeignKey, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

class GrupoFamiliarModel(Base):
    __tablename__ = "grupos_familiares"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamento Bidirecional
    carteiras: Mapped[list["CarteiraModel"]] = relationship(back_populates="grupo_familiar", cascade="all, delete-orphan")


class CarteiraModel(Base):
    __tablename__ = "carteiras"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo: Mapped[str] = mapped_column(nullable=False)
    # Usar o operador '| None' é melhor do que usar 'Optional[str]' pois não precisa importar dependência.
    saldo: Mapped[float | None] = mapped_column(default=0.0)
    grupo_familiar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("grupos_familiares.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamento Bidirecional
    grupo_familiar: Mapped["GrupoFamiliarModel"] = relationship(back_populates="carteiras")


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
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(Brasil_TZ))

    @property
    def created_at(self):
        return self.created_at_utc.astimezone(Brasil_TZ)
