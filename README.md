# Ferreira Finanças API

## Para teste local
- Instalar o TZDATA:

    ``pip install tzdata``

## Custom Start Command
- Custom start command com correção de CORS:

    ``uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --forwarded-allow-ips '*'``

- Sem correção:

    ``uvicorn app.main:app --host 0.0.0.0 --port ${PORT}``

## Alembic
- Criar as migrações no Alembic:

    ``alembic revision --autogenerate -m "DESCRIÇÃO DA MIGRAÇÃO"``

- Aplicar as migrações:
    ``alembic upgrade head``