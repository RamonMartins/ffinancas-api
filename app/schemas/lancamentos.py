# app/schemas/lancamentos.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, StringConstraints, field_serializer
from datetime import datetime
from typing import Annotated
from app.core.config import Brasil_TZ

class LancamentoCreate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    is_active: bool = True

class LancamentoRead(BaseModel):
    id: UUID
    titulo: str
    is_active: bool
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_serializer("created_at", "modified_at")
    def serializar_data(self, dt: datetime):
        dt_brasil = dt.astimezone(Brasil_TZ)
        return dt_brasil.isoformat()

class LancamentoUpdate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    is_active: bool
