# app/schemas/lancamentos.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, StringConstraints, Field
from datetime import datetime
from typing import Annotated

class LancamentoCreate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    is_active: bool = True

class LancamentoRead(BaseModel):
    id: UUID
    titulo: str
    is_active: bool
    created_at_utc: datetime = Field(alias="created_at")

    model_config = ConfigDict(from_attributes=True)

class LancamentoUpdate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    is_active: bool
