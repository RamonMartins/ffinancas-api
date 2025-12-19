# Ferreira Finanças API

## Para teste local
- Instalar o TZDATA:

    ``pip install tzdata``

- Custom start command com correção de CORS:

    ``uvicorn app.main:app --host 0.0.0.0 --port $PORT --forwarded-allow-ips '*'``

- Sem correção:

    ``uvicorn app.main:app --host 0.0.0.0 --port $PORT``