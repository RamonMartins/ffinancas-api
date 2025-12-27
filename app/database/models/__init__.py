# app/database/models/__init__.py

from app.database.base import Base

from .grupos_familiares import GrupoFamiliarModel
from .usuarios import UsuarioModel
from .carteiras import CarteiraModel
from .lancamentos import LancamentoModel

# O __all__ avisa ao Python (e ao Alembic) quais classes são a "cara" deste pacote.
# Isso também remove os avisos de "unused import" no seu editor.
__all__ = [
    "Base",
    "GrupoFamiliarModel",
    "UsuarioModel",
    "CarteiraModel",
    "LancamentoModel"
]