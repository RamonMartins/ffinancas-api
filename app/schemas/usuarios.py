# app/schemas/usuarios.py

from uuid import UUID
from fastapi_users import schemas
from pydantic import ConfigDict

class UsuarioRead(schemas.BaseUser[UUID]):
    nome: str
    lider_familiar: bool
    grupo_familiar_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class UsuarioCreate(schemas.BaseUserCreate):
    nome: str
    lider_familiar: bool
    grupo_familiar_id: UUID | None = None


class UsuarioUpdate(schemas.BaseUserUpdate):
    nome: str | None = None
    lider_familiar: bool | None = None
    grupo_familiar_id: UUID | None = None
