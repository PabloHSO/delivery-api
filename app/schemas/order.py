from pydantic import BaseModel
from typing import List, Optional, Literal

class Order(BaseModel):
    usuario_id: int

    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    quantidade: int
    preco_unitario: float
    sabor: Literal["CALABRESA", "MARGUERITA", "FRANGO_COM_CATUPIRY", "PORTUGUESA", "QUATRO_QUEIJOS"]
    tamanho: Literal["PEQUENA", "MEDIA", "GRANDE"]

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[OrderItem]

    class Config:
        from_attributes = True