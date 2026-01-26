# 🍔 Delivery System API

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green)
![Tests](https://img.shields.io/badge/Tests-Pytest-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-green)

API de backend para um sistema de delivery, construída com **FastAPI**, **Python 3** e **SQLAlchemy**.  
Permite cadastro e autenticação de usuários, criação e gerenciamento de pedidos, e controle de permissões via JWT.

## 📌 GitPage - Delivery API

- 🌐 [Delivery API - GitPage](https://pablohso.github.io/delivery-api/)
- 🌐 [Pablo - GitPage](https://pablohso.github.io/PabloHSO/)

---

## 🚀 Funcionalidades

- Cadastro de usuários (usuário comum e administrador)
- Login com autenticação JWT
- Permissões diferenciadas: usuário vs administrador
- Criação, visualização, atualização e cancelamento de pedidos
- Adição e remoção de itens do pedido
- Endpoints protegidos por autenticação
- Testes unitários e de integração com Pytest
- Cobertura de testes com `pytest-cov`
- Documentação automática via **Swagger** e **OpenAPI**

---

## 🛠 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** – Framework moderno para APIs
- **SQLAlchemy** – ORM para gerenciamento de banco de dados
- **SQLite / PostgreSQL** – Banco de dados relacional
- **Pytest** – Testes unitários e de integração
- **Bcrypt** – Hash seguro de senhas
- **JWT (JOSE)** – Autenticação via tokens

---

## 📦 Estrutura do Projeto

```text
delivery-api/
├─ app/
│  ├─ main.py          # Entrada da aplicação FastAPI
│  ├─ models/          # Models do SQLAlchemy (Usuario, Pedido, ItemPedido)
│  ├─ schemas/         # Schemas Pydantic
│  ├─ services/        # Lógica de negócio (auth_service, order_service)
│  └─ routers/         # Rotas organizadas por módulo
├─ tests/              # Testes unitários e de integração
├─ requirements.txt    # Dependências do projeto
├─ conftest.py         # Fixtures para testes
└─ README.md           # Este arquivo
```
---

## ⚡ Rodando a API Localmente

1. Clone o projeto:

 ```bash
 git clone https://github.com/seu-usuario/delivery-api.git
 cd delivery-api
 ```

---

2. Crie e ative um ambiente virtual

 ```bash
 python -m venv venv
 source venv/bin/activate   # Linux / macOS
 venv\Scripts\activate      # Windows
 ```

---

3. Instale as dependências:

 ```bash
 pip install -r requirements.txt
 ```

---

4. Rodar a aplicação: 
 ```bash
 uvicorn app.main:app --reload
 ```

---  

5. Acesse a documentação:

 - Swagger UI: http://127.0.0.1:8000/docs
 - Redoc: http://127.0.0.1:8000/redoc

---

## 🧪 Executando Testes

 - O projeto possui testes unitários e de integração:

## Para rodar a cobertura completa dos testes 

 ```bash
 pytest --cov=app --cov-report=term-missing
 ```

 - Todos os testes passam ✅
 - Cobertura completa da API demonstrada no terminal.

## 🔑 Exemplos de Uso

 ### Cadastro de usuário (POST /auth/sign-up)

 ```http
  POST /auth/sign-up
  Content-Type: application/json

  {
  "nome": "João",
  "email": "joao@test.com",
  "senha": "123456"
  }
  ```
  Response:

  ```json
  {
   "message": "Usuário criado com sucesso",
   "user_id": 1,
   "email": "joao@test.com"
  }
  ```

 - Obs: Apenas administradores podem criar usuários admin.

 ### Login de usuário (POST /auth/sign-in-form)

  ```http
  POST /auth/sign-in-form
  Content-Type: application/x-www-form-urlencoded

  username=user@test.com
  password=123456
  ```
  Response:

  ```json
  {
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
  }
  ```

 - Use esse token nos headers para acessar endpoints protegidos:

 ### Authorization: Bearer <JWT_TOKEN>

 ## Criar pedido (POST /orders/pedido)

  Request Header:
  
  ```http
  Authorization: Bearer <JWT_TOKEN>
  ```
  Response:

  ```json
  {
  "pedido_id": 1,
  "usuario": 1,
  "status": "ABERTO",
  "itens": []
  }
  ```

 ## Adicionar item ao pedido (POST /orders/pedido/adicionar_item/{pedido_id})

  ```json 
  {
  "quantidade": 2,
  "preco_unitario": 25,
  "sabor": "CALABRESA",
  "tamanho": "MEDIA"
  }
  ```
 Reponse:

 ```json
  {
  "pedido_id": 1,
  "preco_total": 50
  }
 ```

 ## Remover item do pedido (DELETE /orders/pedido/remover_item/{item_id})

  Response:

  ```json
  {
  "pedido_id": 1,
  "preco_atualizado": 0
  }
  ```

 ### Finalizar pedido (POST /orders/pedido/finalizar/{pedido_id})

  Response:

  ```json
  {
  "pedido_id": 1,
  "status": "FINALIZADO"
  }
 ```

 ### Listar pedidos do usuário (GET /orders/meus_pedidos)

  Response:

  ```json
  [
    {
    "pedido_id": 1,
    "status": "FINALIZADO",
    "itens": []
    },
    {
    "pedido_id": 2,
    "status": "ABERTO",
    "itens": [...]
    }
  ]
  ```

 ## 📖 Documentação

 - A documentação da API é gerada automaticamente pelo FastAPI via Swagger/OpenAPI.
 - Swagger UI: http://127.0.0.1:8000/docs
 - Redoc: http://127.0.0.1:8000/redoc

## 🔍 Observações

 - Banco de dados configurado via SQLAlchemy
 - Testes isolados com fixtures no conftest.py
 - Senhas armazenadas de forma segura com Bcrypt
 - Tokens JWT para autenticação de rotas protegidas
 - Pode ser usado localmente ou configurado para PostgreSQL/SQLite em produção
