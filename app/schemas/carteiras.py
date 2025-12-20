# app/schemas/carteiras.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CarteiraCreate(BaseModel):
    titulo: str
    saldo: float | None = 0.0

class CarteiraRead(BaseModel):
    id: UUID
    titulo: str
    saldo: float | None = 0.0
    created_at_utc: datetime = Field(alias="created_at")

    model_config = ConfigDict(from_attributes=True)