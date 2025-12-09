# settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo

class SettingsClass(BaseSettings):
    # O pydantic Settings lida automaticamente com a leitura do .env

    # 1. Variável de Ambiente: Padrão é 'development' se a variável não estiver definida
    ENVIRONMENT: str = "development" 
    
    # 2. Exemplo de Variável de Conexão com DB
    DATABASE_URL: str = "sqlite:///./prod.db"

    # Define de onde carregar as variáveis (padrão do pydantic)
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    FRONT_URL: str = "http://localhost:3000" or "http://127.0.0.1:3000"

# Cria a instância que será importada na aplicação principal
settings = SettingsClass()

# Define o fuso horário do Brasil para uso na aplicação
Brasil_TZ = ZoneInfo("America/Sao_Paulo")