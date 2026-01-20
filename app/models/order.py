from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import Base

# Pedido   
class Pedido(Base):
    __tablename__ = 'pedidos'

    # STATUS_PEDIDO = (
    #     ('PENDENTE', 'PENDENTE'),
    #     ('CANCELADO', 'CANCELADO'),
    #     ('FINALIZADO', 'FINALIZADO'),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # Pendente / Cancelado / Finalizado 
    usuario = Column("usuario_id", ForeignKey("usuarios.id"), nullable=False)
    preco = Column("preco", Float, nullable=False)
    # Relacionamento com ItensPedido
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        # percorrer os itens do pedido e somar os preços e colocar no atributo preco
        # Comprehension de lista para calcular o preço total
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

# ItensPedido
class ItemPedido(Base):
    __tablename__ = 'itens_pedidos'

    # SABORES_PIZZA = (
    #     ('CALABRESA', 'CALABRESA'),
    #     ('MARGUERITA', 'MARGUERITA'),
    #     ('FRANGO_COM_CATUPIRY', 'FRANGO_COM_CATUPIRY'),
    #     ('PORTUGUESA', 'PORTUGUESA'),
    #     ('QUATRO_QUEIJOS', 'QUATRO_QUEIJOS'),
    # )

    # TAMANHOS_PIZZA = (
    #     ('PEQUENA', 'PEQUENA'),
    #     ('MEDIA', 'MEDIA'),
    #     ('GRANDE', 'GRANDE'),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    pedido = Column("pedido", ForeignKey("pedidos.id"), nullable=False)
    quantidade = Column("quantidade", Integer, nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    sabor = Column("sabor", String, nullable=False)
    tamanho = Column("tamanho", String, nullable=False)

    def __init__(self, pedido, quantidade, preco_unitario, sabor, tamanho):
        self.pedido = pedido
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.sabor = sabor
        self.tamanho = tamanho

# alembic init alembic criar pasta de migrações e o arqquivo alembic.ini
# alembic revision --autogenerate -m "initial migration" criar a migração inicial
# alembic upgrade head aplicar as migrações no banco de dados (No momento da erro por falta da dependência sqlalchemy-utils)

# Caso seja necessário editar algo nas tabelas, criar uma nova migração com: alembic revision --autogenerate -m "descrição da modificação"
# Após só rodar alembic upgrade head para aplicar as mudanças no banco de dados