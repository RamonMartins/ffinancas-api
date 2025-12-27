# app/database/models/usuarios.py

import uuid
from sqlalchemy import ForeignKey, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import Brasil_TZ, settings
from datetime import datetime
from app.database.base import Base


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