# app/schemas/grupos_familiares.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, StringConstraints, field_serializer
from datetime import datetime
from typing import Annotated
from app.core.config import Brasil_TZ

class GrupoFamiliarCreate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class GrupoFamiliarRead(BaseModel):
    id: UUID
    titulo: str
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_serializer("created_at", "modified_at")
    def serializar_data(self, dt: datetime):
        dt_brasil = dt.astimezone(Brasil_TZ)
        return dt_brasil.isoformat()

class GrupoFamiliarUpdate(BaseModel):
    titulo: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1)] = None
