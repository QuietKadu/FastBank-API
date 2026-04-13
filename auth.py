from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status

# Essa chave é o SEGREDO. No mundo real, você não deixa ela no código.
SECRET_KEY = "sua_chave_secreta_muito_braba" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def criar_token_acesso(data: dict):
    dados_para_criptografar = data.copy()
    
    # Define quando o crachá (token) vence
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_criptografar.update({"exp": expiracao})
    
    # Gera a sopa de letrinhas (JWT)
    token_jwt = jwt.encode(dados_para_criptografar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verificar_token(token: str):
    try:
        # Tenta "abrir" o token usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload # Se deu certo, retorna os dados do usuário (ex: o nome)
    except JWTError:
        # SE MUDAR UMA LETRA NO INSOMNIA, CAI AQUI!
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )