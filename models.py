from typing import Optional
from sqlmodel import Field, SQLModel
import datetime

class BankRead(SQLModel):
    id: int # É bom ter o ID no Read para o usuário saber qual é
    type: str
    amount: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now) # Adicionamos um timestamp para saber quando a transação foi criada

class BankCreate(SQLModel):
    type: str = Field(
        min_length=3, 
        description="Tipo da operação: 'deposit' para depósito ou 'withdrawal' para saque"
    )
    amount: float = Field(
        gt=0, 
        description="Valor da transação. Deve ser maior que zero."
    )
class Bank(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id") # Para saber quem fez a transação
    type: str
    amount: float

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    senha_hash: str

class UsuarioCreate(SQLModel):
    username: str
    password: str