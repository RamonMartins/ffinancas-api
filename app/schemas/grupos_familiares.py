# app/schemas/grupos_familiares.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, StringConstraints, field_serializer, field_validator
from datetime import datetime
from typing import Annotated
from app.core.config import Brasil_TZ

class GrupoFamiliarCreate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class GrupoFamiliarRead(BaseModel):
    id: UUID
    titulo: str
    carteiras: list[UUID] = []
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_validator("carteiras", mode="before")
    @classmethod
    def serializar_carteiras(cls, list_carteiras: any):
        nova_list_carteiras = []

        for item in list_carteiras:
            if hasattr(item, "id"):
                nova_list_carteiras.append(item.id)
            else:
                nova_list_carteiras.append(item)
        
        return nova_list_carteiras

    @field_serializer("created_at", "modified_at")
    def serializar_data(self, dt: datetime):
        dt_brasil = dt.astimezone(Brasil_TZ)
        return dt_brasil.isoformat()

class GrupoFamiliarUpdate(BaseModel):
    titulo: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1)] = None
