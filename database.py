from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)

# Essa função cria as tabelas
def criar_banco():
    SQLModel.metadata.create_all(engine)

# Essa função gerencia as sessões
def get_session() -> Generator:
    with Session(engine) as session:
        yield session