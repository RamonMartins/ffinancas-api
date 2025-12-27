# app/database/models/grupos_familiares.py

import uuid
from sqlalchemy import ForeignKey, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .carteiras import CarteiraModel


class GrupoFamiliarModel(Base):
    __tablename__ = "grupos_familiares"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamento Bidirecional
    carteiras: Mapped[list["CarteiraModel"]] = relationship("CarteiraModel", back_populates="grupo_familiar", cascade="all, delete-orphan")