# Pydantic faz a validação de dados e a serialização/deserialização (Velocidade e Integridade)
from pydantic import BaseModel
from typing import List, Optional, Literal

class UserCreate(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    # Configuração para permitir a criação do modelo a partir de objetos ORM (como os modelos do SQLAlchemy)
    class Config:
        from_attributes = True
