# app/main.py
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Inclui rotas da versão 1
app.include_router(api_router, prefix="/pluvio-api")

# Rota simples de teste
@app.get("/")
def root():
    return {"message": "API em execução 🚀"}
