from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base

# Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    # Criar as colunas da tabela
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(100), nullable=False)
    email = Column("email", String(100), unique=True, nullable=False)
    senha = Column("senha", String(100), nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    # Ao criar um novo usuario 
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

    def __repr__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, email={self.email}, ativo={self.ativo}, admin={self.admin})"
