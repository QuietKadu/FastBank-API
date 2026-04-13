🏦 FastBank API
API assíncrona para gerenciamento de transações bancárias (depósitos e saques) com autenticação JWT, desenvolvida em Python utilizando FastAPI e SQLModel.

🚀 Link do Deploy
Acesse a API rodando em tempo real: https://fastbank-api.onrender.com/docs

🛠️ Tecnologias Utilizadas
FastAPI: Framework moderno e rápido.

SQLModel: Interação com o banco de dados SQLite de forma simples.

JWT (JSON Web Tokens): Segurança e autenticação de usuários.

Poetry: Gerenciamento de dependências e ambiente virtual.

Uvicorn: Servidor ASGI para alta performance.

📋 Requisitos do Desafio (Checklist)
[x] CRUD de Transações (Depósitos e Saques).

[x] Autenticação e Autorização (JWT).

[x] Validação de saldo suficiente para saques.

[x] Relacionamento entre Usuário e Transação.

[x] Deploy realizado no Render.

[x] Código utilizando async e await.

🔧 Como rodar o projeto localmente
Clone o repositório:

Bash
git clone https://github.com/QuietKadu/FastBank-API.git
cd FastBank-API
Instale as dependências (via Poetry):

Bash
poetry install
Inicie o servidor:

Bash
poetry run uvicorn main:app --reload
Acesse no navegador:
http://127.0.0.1:8000/docs
