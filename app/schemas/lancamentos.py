# app/schemas/lancamentos.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class LancamentoCreate(BaseModel):
    titulo: str
    is_active: bool = True

class LancamentoRead(BaseModel):
    id: UUID
    titulo: str
    is_active: bool
    created_at_utc: datetime = Field(alias="created_at")

    model_config = ConfigDict(from_attributes=True)

class LancamentoUpdate(BaseModel):
    titulo: str
    is_active: bool
