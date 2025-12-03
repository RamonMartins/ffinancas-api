from fastapi import APIRouter

roteador = APIRouter(prefix="/lancamentos", tags=["Lançamentos"])

# Rota completa será: "/lancamentos/"
@roteador.get("/")
async def listar_usuarios():
    return [{"nome": "Marcos"}, {"nome": "Leonardo"}]

@roteador.get("/me")
async def usuario_atual():
    return {"nome": "Usuário atual"}