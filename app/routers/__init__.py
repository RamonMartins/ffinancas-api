# app/routers/__init__.py

from fastapi import APIRouter
from .grupos_familiares import roteador as grupos_roteador
from .carteiras import roteador as carteiras_roteador
from .lancamentos import roteador as lancamento_roteador


rotas_projeto = APIRouter()

rotas_projeto.include_router(grupos_roteador)
rotas_projeto.include_router(carteiras_roteador)
rotas_projeto.include_router(lancamento_roteador)