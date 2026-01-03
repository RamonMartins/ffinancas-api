# app/database/models/usuarios.py

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, DateTime, UUID, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database.base import Base


class UsuarioModel(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "usuarios"

    # Campos adicionados pelo FastAPI Users
    # id(UUID), email(EmailStr), hashed_password, is_active(bool), is_superuser(bool), is_verified(bool)
    nome: Mapped[str] = mapped_column(nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    