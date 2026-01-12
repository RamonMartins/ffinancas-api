# app/database/models/usuarios.py

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, DateTime, UUID, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .grupos_familiares import GrupoFamiliarModel


class UsuarioModel(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "usuarios"

    # Campos adicionados pelo FastAPI Users
    # id(UUID), email(EmailStr), hashed_password, is_active(bool), is_superuser(bool), is_verified(bool)
    nome: Mapped[str] = mapped_column(nullable=False)
    lider_familiar: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    grupo_familiar_id: Mapped[UUID | None] = mapped_column(ForeignKey("grupos_familiares.id", ondelete="SET NULL"), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamento Bidirecional
    grupo_familiar: Mapped["GrupoFamiliarModel"] = relationship("GrupoFamiliarModel", back_populates="usuarios")
