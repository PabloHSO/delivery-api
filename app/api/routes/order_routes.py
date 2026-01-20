from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_session
from app.core.deps import get_current_user
from app.models.user import Usuario
from app.schemas.order import OrderItem, ResponsePedidoSchema
from app.services import order_service

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


# -------------------------------------------------
# Rota base
# -------------------------------------------------
@order_router.get("/")
def orders_home(
    user: Usuario = Depends(get_current_user)
):
    """
    Rota base do módulo de pedidos.

    Todas as rotas exigem autenticação.
    """
    return {
        "message": "Módulo de pedidos ativo",
        "user_id": user.id
    }


# -------------------------------------------------
# Criar pedido
# -------------------------------------------------
@order_router.post(
    "/pedido",
    status_code=status.HTTP_201_CREATED
)
def create_order(
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Cria um novo pedido para o usuário autenticado.
    """
    pedido = order_service.create_order(db, user)
    return {
        "message": "Pedido criado com sucesso",
        "pedido_id": pedido.id
    }


# -------------------------------------------------
# Cancelar pedido
# -------------------------------------------------
@order_router.post("/pedido/cancelar/{pedido_id}")
def cancel_order(
    pedido_id: int,
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Cancela um pedido existente.
    """
    pedido = order_service.cancel_order(db, pedido_id, user)
    return {
        "message": "Pedido cancelado com sucesso",
        "status": pedido.status
    }


# -------------------------------------------------
# Finalizar pedido
# -------------------------------------------------
@order_router.post("/pedido/finalizar/{pedido_id}")
def finalize_order(
    pedido_id: int,
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Finaliza um pedido.
    """
    pedido = order_service.finalize_order(db, pedido_id, user)
    return {
        "message": "Pedido finalizado com sucesso",
        "status": pedido.status
    }


# -------------------------------------------------
# Listar pedidos (admin)
# -------------------------------------------------
@order_router.get("/listar")
def list_orders(
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Lista todos os pedidos do sistema (admin).
    """
    return order_service.list_all_orders(db, user)


# -------------------------------------------------
# Pedidos do usuário autenticado
# -------------------------------------------------
@order_router.get(
    "/meus_pedidos",
    response_model=List[ResponsePedidoSchema]
)
def view_my_orders(
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Lista os pedidos do usuário autenticado.
    """
    return order_service.list_user_orders(db, user)


# -------------------------------------------------
# Visualizar pedido especiífico
# -------------------------------------------------
@order_router.get(
    "/pedido/{pedido_id}",
    response_model=ResponsePedidoSchema
)
def view_order(
    pedido_id: int,
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Visualiza um pedido específico.
    """
    return order_service.get_order_by_id(db, pedido_id, user)


# -------------------------------------------------
# Adicionar item
# -------------------------------------------------
@order_router.post("/pedido/adicionar_item/{pedido_id}")
def add_item(
    pedido_id: int,
    item: OrderItem,
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Adiciona um item ao pedido.
    """
    pedido = order_service.add_item_to_order(db, pedido_id, item, user)
    return {
        "message": "Item adicionado com sucesso",
        "preco_total": pedido.preco
    }


# -------------------------------------------------
# Remover item
# -------------------------------------------------
@order_router.delete("/pedido/remover_item/{item_id}")
def remove_item(
    item_id: int,
    db: Session = Depends(get_session),
    user: Usuario = Depends(get_current_user)
):
    """
    Remove um item do pedido.
    """
    pedido = order_service.remove_item_from_order(db, item_id, user)
    return {
        "message": "Item removido com sucesso",
        "preco_total": pedido.preco
    }
