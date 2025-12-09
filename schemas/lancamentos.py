# Schema
from pydantic import BaseModel, Field
from datetime import datetime

class LancamentoCreate(BaseModel):
    titulo: str
    is_active: bool = True

class LancamentoRead(BaseModel):
    id: int
    titulo: str
    is_active: bool
    created_at: datetime = Field(alias="created_at_brasil")

    class Config:
        from_attributes = True

class LancamentoUpdate(BaseModel):
    titulo: str
    is_active: bool