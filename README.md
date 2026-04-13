# 🏦 FastBank API

API assíncrona para gerenciamento de transações bancárias (depósitos e saques) com autenticação JWT, desenvolvida em **Python** utilizando **FastAPI** e **SQLModel**.

## 🚀 Link do Deploy
Acesse a API rodando em tempo real: [https://fastbank-api.onrender.com/docs](https://fastbank-api.onrender.com/docs)

## 🛠️ Tecnologias Utilizadas
* **FastAPI**: Framework moderno e de alta performance.
* **SQLModel**: Interação com o banco de dados SQLite.
* **JWT (JSON Web Tokens)**: Segurança e autenticação.
* **Poetry**: Gerenciamento de dependências e ambientes virtuais.
* **Uvicorn**: Servidor ASGI para execução da aplicação.

## 📋 Requisitos do Desafio
- [x] CRUD de Transações (Depósitos e Saques).
- [x] Autenticação e Autorização (JWT).
- [x] Validação de saldo suficiente para saques.
- [x] Relacionamento entre Usuário e Transação.
- [x] Deploy realizado no Render.
- [x] Código utilizando `async` e `await`.

## 🔧 Como rodar o projeto localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/QuietKadu/FastBank-API.git](https://github.com/QuietKadu/FastBank-API.git)
   cd FastBank-API
   2. **Instale as dependências:**
   pip install poetry
   poetry install
   3. **Inicie o servidor:**   
   poetry run uvicorn main:app --reload
   4. **Acesse a documentação:**
   http://127.0.0.1:8000/docsD
   
