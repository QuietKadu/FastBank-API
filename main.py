from fastapi import FastAPI
from database import criar_banco # Agora vem de database.py
from rotas import router as bank_router

app = FastAPI(
    title="Sistema Bancário API",
    description="API para gerenciamento de transações bancárias, depósitos e saques com autenticação JWT.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    criar_banco()

app.include_router(bank_router, prefix="/bank", tags=["Bank"])