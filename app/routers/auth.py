# app/routers/auth.py

from fastapi import APIRouter
from app.core.auth import auth_backend, fastapi_users
from app.schemas.usuarios import UsuarioRead, UsuarioCreate

roteador = APIRouter(prefix="/auth", tags=["Autenticação"])


#--------------------------
# POST - Fazer login
# Rota: POST "/auth/login"
#--------------------------

#--------------------------
# POST - Fazer logout
# Rota: POST "/auth/logout"
#--------------------------
roteador.include_router(
    fastapi_users.get_auth_router(auth_backend)
)


#--------------------------
# POST - Cadastrar usuário
# Rota: POST "/auth/register"
#--------------------------
roteador.include_router(
    fastapi_users.get_register_router(UsuarioRead, UsuarioCreate)
)


#--------------------------
# POST - Gera token se e-mail enviado existe
# Rota: POST "/auth/forgot-password"
#--------------------------

#--------------------------
# POST - Recebe o token e a nova senha para efetivar a alteração da senha
# Rota: POST "/auth/reset-password"
#--------------------------
roteador.include_router(
    fastapi_users.get_reset_password_router()
)
