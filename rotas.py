from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from database import get_session
from models import Bank, BankCreate, BankRead, Usuario, UsuarioCreate
from typing import Optional, List
from passlib.context import CryptContext
from auth import criar_token_acesso, verificar_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- DEPENDÊNCIA DE SEGURANÇA ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    return username

# --- ROTAS DE USUÁRIO ---
@router.post("/usuarios")
async def criar_usuario(user_data: UsuarioCreate, session: Session = Depends(get_session)):
    hash_da_senha = pwd_context.hash(user_data.password)
    novo_usuario = Usuario(username=user_data.username, senha_hash=hash_da_senha)
    await run_in_threadpool(session.add, novo_usuario)
    await run_in_threadpool(session.commit)
    return {"message": "Usuário criado com sucesso!"}

@router.post("/login")
async def login(user_data: UsuarioCreate, session: Session = Depends(get_session)):
    usuario = await run_in_threadpool(
        lambda: session.exec(select(Usuario).where(Usuario.username == user_data.username)).first()
    )

    if not usuario or not pwd_context.verify(user_data.password, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    
    token = criar_token_acesso(data={"sub": usuario.username})
    return {"access_token": token, "token_type": "bearer"}

# --- ROTAS BANCÁRIAS (REQUISITOS DO DESAFIO) ---

@router.get("/", response_model=List[BankRead])
async def listar_extrato(session: Session = Depends(get_session), usuario_atual: str = Depends(get_current_user)):
    # Requisito: Exibição de Extrato (apenas do dono da conta)
    usuario = await run_in_threadpool(
        lambda: session.exec(select(Usuario).where(Usuario.username == usuario_atual)).first()
    )

    statement = select(Bank).where(Bank.usuario_id == usuario.id)
    extrato = await run_in_threadpool(lambda: session.exec(statement).all())
    return extrato

@router.post(
    "/transactions", 
    response_model=BankRead,
    summary="Registrar nova transação",
    description="Cria um registro de depósito ou saque. Se for saque, o sistema valida se há saldo suficiente."
)

async def adicionar_transacao(bank_input: BankCreate, session: Session = Depends(get_session), usuario_atual: str = Depends(get_current_user)):
    # Requisito: Cadastro de Transações e Relacionamento
    usuario = await run_in_threadpool(
        lambda: session.exec(select(Usuario).where(Usuario.username == usuario_atual)).first()
    )
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Requisito: Validação de Saldo para Saque
    if bank_input.type.lower() == "withdrawal":
        transacoes = await run_in_threadpool(
            lambda: session.exec(select(Bank).where(Bank.usuario_id == usuario.id)).all()
        )

        saldo_atual = sum(t.amount if t.type.lower() == "deposit" else -t.amount for t in transacoes)
        
        if bank_input.amount > saldo_atual:
            raise HTTPException(status_code=400, detail=f"Saldo insuficiente. Saldo: R$ {saldo_atual:.2f}")

    novo_item = Bank(type=bank_input.type, amount=bank_input.amount, usuario_id=usuario.id)
    await run_in_threadpool(session.add, novo_item)
    await run_in_threadpool(session.commit)
    await run_in_threadpool(session.refresh, novo_item)
    return novo_item

@router.get("/{id}", response_model=BankRead)
async def obter_detalhe(id: int, session: Session = Depends(get_session), usuario_atual: str = Depends(get_current_user)):
    usuario = await run_in_threadpool(
        lambda: session.exec(select(Usuario).where(Usuario.username == usuario_atual)).first()
    )

    transacao = await run_in_threadpool(session.get, Bank, id)

    # Segurança: Não deixa ver transação de outro usuário
    if not transacao or transacao.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Não encontrado")
    
    return transacao