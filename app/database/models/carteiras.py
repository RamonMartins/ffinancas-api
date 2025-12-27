# app/database/models/carteiras.py

import uuid
from sqlalchemy import ForeignKey, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .grupos_familiares import GrupoFamiliarModel


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
    grupo_familiar: Mapped["GrupoFamiliarModel"] = relationship("GrupoFamiliarModel", back_populates="carteiras")
