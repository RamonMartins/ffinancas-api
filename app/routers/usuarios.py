# app/routers/usuarios.py

from fastapi import APIRouter
from app.core.auth import fastapi_users
from app.schemas.usuarios import UsuarioRead, UsuarioUpdate

roteador = APIRouter(prefix="/usuarios", tags=["Usuários"])


#--------------------------
# GET - Ver dados do meu perfil (usuário logado)
# Rota: GET "/usuarios/me"
#--------------------------

#--------------------------
# PATCH - Atualizar meus próprios dados
# Rota: PATCH "/usuarios/me"
#--------------------------

#--------------------------
# GET - Ver detalhes de um usuário específico (Apenas Superuser)
# Rota: GET "/usuarios/{id}"
#--------------------------

#--------------------------
# PATCH - Atualizar dados de um usuário específico (Apenas Superuser)
# Rota: PATCH "/usuarios/{id}"
#--------------------------

#--------------------------
# DELETE - Excluir um usuário do sistema (Apenas Superuser)
# Rota: DELETE "/usuarios/{id}"
#--------------------------
roteador.include_router(
    fastapi_users.get_users_router(UsuarioRead, UsuarioUpdate)
)
