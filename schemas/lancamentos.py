# Schema
from pydantic import BaseModel
from datetime import datetime

class LancamentoCreate(BaseModel):
    titulo: str
    is_active: bool = True

class LancamentoRead(BaseModel):
    id: int
    titulo: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode= True

class LancamentoUpdate(BaseModel):
    titulo: str
    is_active: bool