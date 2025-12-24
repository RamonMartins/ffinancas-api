# app/schemas/carteiras.py

from uuid import UUID
from pydantic import BaseModel, ConfigDict, StringConstraints, Field
from datetime import datetime
from typing import Annotated

class CarteiraCreate(BaseModel):
    titulo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    saldo: float | None = 0.0

class CarteiraRead(BaseModel):
    id: UUID
    titulo: str
    saldo: float | None = 0.0
    created_at_utc: datetime = Field(alias="created_at")
    teste_data: datetime

    model_config = ConfigDict(from_attributes=True)