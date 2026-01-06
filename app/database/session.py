# app/database/session.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# 1. Definição da URL do Banco de Dados vinda das configurações
BD_URL = settings.DATABASE_URL

if BD_URL.startswith("postgresql://"):
    BD_URL = BD_URL.replace("postgresql://", "postgresql+asyncpg://")

## 2. Configuração do Engine (Motor de conexão)
if settings.ENVIRONMENT == "development":
    # No SQLite local, precisamos do check_same_thread=False para o FastAPI
    engine = create_async_engine(
        BD_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # No PostgreSQL (Produção/Railway), usamos configurações de resiliência
    engine = create_async_engine(
        BD_URL,
        pool_pre_ping=True,      # Testa se a conexão está "viva" antes de cada consulta
        pool_recycle=300,        # Descarta conexões com mais de 5 min para evitar que fiquem "velhas"
    )

# 3. Gerador de Sessões Assíncronas
# Cada instância de SessionLocal será uma sessão de banco de dados.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 4. Função de Retentativa (A "Capa" de inteligência)
# Se o banco estiver suspendido (Cold Start), esta lógica impede que a API falhe de imediato.
@retry(
    stop=stop_after_attempt(8),      # Limita a no máximo 5 tentativas
    wait=wait_fixed(3),              # Espera exatamente 3 segundos entre cada tentativa
    retry=retry_if_exception_type((
        OperationalError,  # Erro de operação do banco (offline/refused)
        OSError,           # Erro de rede (host unreachable)
        ConnectionError,   # Erro de conexão TCP
        EOFError           # Conexão fechada prematuramente
    )), # Só tenta de novo se for erro de conexão/rede
    reraise=True                     # Se esgotar as 5 tentativas, lança o erro final
)
async def get_db_session_with_retry():
    # Tenta abrir uma sessão e validar se o banco está acordado.
    db = AsyncSessionLocal()  # Cria a instância da sessão
    try:
        # O "SELECT 1" é o teste real. Se o banco estiver dormindo, esta linha falha
        # e ativa o decorador @retry acima para tentar novamente.
        await db.execute(text("SELECT 1"))
        return db
    except Exception as e:
        # Se falhar (ex: banco offline), fecha a sessão mal-sucedida e lança o erro
        await db.close()
        raise e

# 5. Função que será usada como uma 'Dependência' no FastAPI
async def get_db():
    # Função injetada nos endpoints via Depends(get_db).
    # Garante que a sessão seja aberta com retry e fechada ao final da requisição.
    db = None
    try:
        # Chama a função que tem a lógica de retentativa
        db = await get_db_session_with_retry()
        yield db        # Entrega a sessão pronta para o endpoint usar
    finally:
        # O 'finally' garante que, mesmo que o endpoint dê erro, a conexão seja fechada
        if db:
            await db.close()