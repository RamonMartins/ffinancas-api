# app/core/auth.py

from uuid import UUID
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from app.core.users_db import get_user_db
from app.database.models.usuarios import UsuarioModel
from app.core.config import settings


# 1. Transporte - Como o token chega (via Header "Authorization: Bearer ...")
bearer_transport = BearerTransport(tokenUrl="auth/login")

# 2. Estratégia - Como o token é gerado
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=86400      # Token válido por 24 horas
    )

# 3. Backend de Autenticação
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# 4. Gestor (UserManager) - Lógica de criação de user
class UserManager(BaseUserManager[UsuarioModel, UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    def parse_id(self, value: str) -> UUID:
        return UUID(value)

    async def on_after_register(self, user: UsuarioModel, token: str, request: Optional[Request] = None):
        print(f"Utilizador {user.nome} registado com sucesso.")
    
    async def on_after_forgot_password(self, user: UsuarioModel, token: str, request: Optional[Request] = None):
        # Aqui você enviaria o e-mail para o usuário
        print(f"O utilizador {user.email} solicitou reset. Token: {token}")
        # O link enviado no e-mail seria algo como: 
        # https://meusite.com/reset-password?token={token}

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# Objeto principal para usar nos Routers
fastapi_users = FastAPIUsers[UsuarioModel, UUID](
    get_user_manager,
    [auth_backend],
)

# Atalho para proteger rotas: current_user
current_user = fastapi_users.current_user(active=True)
current_user_superuser = fastapi_users.current_user(active=True, superuser=True)
