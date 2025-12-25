# app/schemas/carteiras.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, StringConstraints, Field, field_serializer
from datetime import datetime
from typing import Annotated
from app.core.config import Brasil_TZ

class CarteiraCreate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    saldo: float | None = 0.0

class CarteiraRead(BaseModel):
    id: UUID
    titulo: str
    saldo: float | None = 0.0
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_serializer("created_at", "modified_at")
    def serializar_data(self, dt: datetime):
        # Converte de UTC para Brasil
        dt_brasil = dt.astimezone(Brasil_TZ)
        # Retorna no formato ISO 8601 com o fuso -03:00 (em vez de Z)
        return dt_brasil.isoformat()
        # Opcional: Se preferir formato brasileiro "24/12/2025 20:30:00", use:
        # return dt_brazil.strftime("%d/%m/%Y %H:%M:%S")

class CarteiraUpdate(BaseModel):
    titulo: Annotated[str | None, StringConstraints(strip_whitespace=True, min_length=1)] = None
    saldo: float | None = 0.0
