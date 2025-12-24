# app/database/database.py

from app.core.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

# 1. Definição da URL do Banco de Dados vinda das configurações
BD_URL = settings.DATABASE_URL

## 2. Configuração do Engine (Motor de conexão)
if settings.ENVIRONMENT == "development":
    # No SQLite local, precisamos do check_same_thread=False para o FastAPI
    engine = create_engine(
        BD_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # No PostgreSQL (Produção/Railway), usamos configurações de resiliência
    engine = create_engine(
        BD_URL,
        pool_pre_ping=True,      # Testa se a conexão está "viva" antes de cada consulta
        pool_recycle=300,        # Descarta conexões com mais de 5 min para evitar que fiquem "velhas"
        connect_args={"connect_timeout": 10} # Tempo máximo de espera para abrir a conexão inicial
        )

# 3. SessionLocal será a classe de sessão real do banco de dados.
# Cada instância de SessionLocal será uma sessão de banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base é a classe base para criar os modelos de banco de dados (tabelas).
Base = declarative_base()

# 5. Função de Retentativa (A "Capa" de inteligência)
# Se o banco estiver suspendido (Cold Start), esta lógica impede que a API falhe de imediato.
@retry(
    stop=stop_after_attempt(5),      # Limita a no máximo 5 tentativas
    wait=wait_fixed(3),              # Espera exatamente 3 segundos entre cada tentativa
    retry=retry_if_exception_type(OperationalError), # Só tenta de novo se for erro de conexão/rede
    reraise=True                     # Se esgotar as 5 tentativas, lança o erro final
)
def get_db_session_with_retry():
    # Tenta abrir uma sessão e validar se o banco está acordado.
    db = SessionLocal()  # Cria a instância da sessão
    try:
        # O "SELECT 1" é o teste real. Se o banco estiver dormindo, esta linha falha
        # e ativa o decorador @retry acima para tentar novamente.
        db.execute(text("SELECT 1"))
        return db
    except Exception as e:
        # Se falhar (ex: banco offline), fecha a sessão mal-sucedida e lança o erro
        db.close()
        raise e

# 6. Função que será usada como uma 'Dependência' no FastAPI
def get_db():
    # Função injetada nos endpoints via Depends(get_db).
    # Garante que a sessão seja aberta com retry e fechada ao final da requisição.
    db = None
    try:
        # Chama a função que tem a lógica de retentativa
        db = get_db_session_with_retry()
        yield db        # Entrega a sessão pronta para o endpoint usar
    finally:
        # O 'finally' garante que, mesmo que o endpoint dê erro, a conexão seja fechada
        if db:
            db.close()