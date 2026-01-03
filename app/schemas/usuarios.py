# app/schemas/usuarios.py

from uuid import UUID
from fastapi_users import schemas
from pydantic import ConfigDict

class UsuarioRead(schemas.BaseUser[UUID]):
    nome: str
    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(schemas.BaseUserCreate):
    nome: str

class UsuarioUpdate(schemas.BaseUserUpdate):
    nome: str | None = None
