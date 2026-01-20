from sqlalchemy.orm import Session
from app.models.order import Pedido, ItemPedido
from app.models.user import Usuario
from app.schemas.order import OrderItem
from app.core.exceptions import ForbiddenException, NotFoundException


# -------------------------------
# Criar pedido
# -------------------------------
def create_order(
    db: Session,
    user: Usuario
) -> Pedido:
    pedido = Pedido(usuario=user.id)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


# -------------------------------
# Cancelar pedido
# -------------------------------
def cancel_order(
    db: Session,
    pedido_id: int,
    user: Usuario
) -> Pedido:
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise NotFoundException("Pedido não encontrado")

    if not user.admin and pedido.usuario != user.id:
        raise ForbiddenException("Você não tem permissão para cancelar este pedido")

    pedido.status = "CANCELADO"
    db.commit()
    return pedido


# -------------------------------
# Finalizar pedido
# -------------------------------
def finalize_order(
    db: Session,
    pedido_id: int,
    user: Usuario
) -> Pedido:
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise NotFoundException("Pedido não encontrado")

    if not user.admin and pedido.usuario != user.id:
        raise ForbiddenException("Você não tem permissão para finalizar este pedido")

    pedido.status = "FINALIZADO"
    db.commit()
    return pedido


# -------------------------------
# Listar todos pedidos (admin)
# -------------------------------
def list_all_orders(
    db: Session,
    user: Usuario
):
    if not user.admin:
        raise ForbiddenException("Apenas administradores podem acessar esta rota")

    return db.query(Pedido).all()


# -------------------------------
# Listar pedidos do usuário
# -------------------------------
def list_user_orders(
    db: Session,
    user: Usuario
):
    return db.query(Pedido).filter(Pedido.usuario == user.id).all()


# -------------------------------
# Buscar pedido por id (com permissão)
# -------------------------------
def get_order_by_id(
    db: Session,
    pedido_id: int,
    user: Usuario
) -> Pedido:
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise NotFoundException("Pedido não encontrado")

    if not user.admin and pedido.usuario != user.id:
        raise ForbiddenException("Você não tem permissão para acessar este pedido")

    return pedido


# -------------------------------
# Adicionar item ao pedido
# -------------------------------
def add_item_to_order(
    db: Session,
    pedido_id: int,
    item_data: OrderItem,
    user: Usuario
) -> Pedido:
    pedido = get_order_by_id(db, pedido_id, user)

    item = ItemPedido(
        pedido=pedido.id,
        quantidade=item_data.quantidade,
        preco_unitario=item_data.preco_unitario,
        sabor=item_data.sabor,
        tamanho=item_data.tamanho
    )

    db.add(item)
    db.commit()

    pedido.calcular_preco()
    db.commit()

    return pedido


# -------------------------------
# Remover item do pedido
# -------------------------------
def remove_item_from_order(
    db: Session,
    item_id: int,
    user: Usuario
) -> Pedido:
    item = db.query(ItemPedido).filter(ItemPedido.id == item_id).first()
    if not item:
        raise NotFoundException("Item não encontrado")

    pedido = db.query(Pedido).filter(Pedido.id == item.pedido).first()
    if not user.admin and pedido.usuario != user.id:
        raise ForbiddenException("Você não tem permissão para alterar este pedido")

    db.delete(item)
    db.commit()

    pedido.calcular_preco()
    db.commit()

    return pedido
