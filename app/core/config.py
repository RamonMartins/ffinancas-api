# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo

class SettingsClass(BaseSettings):
    # O pydantic Settings lida automaticamente com a leitura do .env

    # Variável do Ambiente (development, production, etc)
    ENVIRONMENT: str
    
    # Variável de conexão à base de dados
    DATABASE_URL: str

    # Variável da Secret Auth - Assina o crachá de entrada (Login)
    JWT_SECRET: str

    # Variável da Secret Auth - Assina o pedido de nova senha
    RESET_PASSWORD_SECRET: str

    # Variável da Secret Auth - Assina o pedido de confirmação de dono do e-mail
    VERIFICATION_TOKEN_SECRET: str

    # Define de onde carregar as variáveis (padrão do pydantic)
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

# Cria a instância que será importada na aplicação principal
settings = SettingsClass()

# Define o fuso horário do Brasil para uso na aplicação
Brasil_TZ = ZoneInfo("America/Sao_Paulo")