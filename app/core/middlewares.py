from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI):
    """
    Configura o CORS da aplicação.
    Permite que frontends externos acessem a API.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ajuste em produção
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
