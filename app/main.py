# app/main.py
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost:8080",
    "http://192.168.1.18:8080",# Exemplo: frontend local (Vite)
    "http://172.27.94.114:8080",
    "http://10.255.255.254:8080",
    "*.ngrok-free.dev"# Exemplo: frontend local (Vite)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # ✅ somente essas origens terão acesso
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Métodos permitidos
    allow_headers=["*"],            # Pode restringir se quiser: ["Authorization", "Content-Type"]
)

# Inclui rotas da versão 1
app.include_router(api_router, prefix="/pluvio-api")

# Rota simples de teste
@app.get("/")
def root():
    return {"message": "API em execução 🚀"}
