import pytest
from app.services.order_service import (
    create_order,
    cancel_order,
    finalize_order,
    list_all_orders,
    list_user_orders,
    get_order_by_id,
    add_item_to_order,
    remove_item_from_order,
)
from app.models.user import Usuario
from app.models.order import Pedido, ItemPedido
from app.schemas.order import OrderItem
from app.core.exceptions import ForbiddenException, NotFoundException

# ----------------------------------------
# Testes unitários para o serviço de pedidos
# ----------------------------------------

# ----------------------------------------
# Criar pedido com sucesso
# Deve criar pedido com status PENDENTE e preço inicial 0
# ----------------------------------------
def test_create_order_success(db_session, user):
    pedido = create_order(db=db_session, user=user)

    assert pedido.id is not None
    assert pedido.usuario == user.id
    assert pedido.status == "PENDENTE"
    assert pedido.preco == 0


# ----------------------------------------
# Cancelar pedido com sucesso
# Dono do pedido pode cancelar
# ----------------------------------------
def test_cancel_order_success(db_session, user):
    pedido = create_order(db_session, user)

    pedido_cancelado = cancel_order(
        db=db_session,
        pedido_id=pedido.id,
        user=user
    )

    assert pedido_cancelado.status == "CANCELADO"


# ----------------------------------------
# Cancelar pedido inexistente
# Deve lançar NotFoundException
# ----------------------------------------
def test_cancel_order_not_found(db_session, user):
    with pytest.raises(NotFoundException):
        cancel_order(
            db=db_session,
            pedido_id=999,
            user=user
        )


# ----------------------------------------
# Cancelar pedido sem permissão
# Usuário que não é dono nem admin não pode cancelar
# ----------------------------------------
def test_cancel_order_forbidden(db_session, user):
    other_user = Usuario(
        nome="Outro",
        email="outro@test.com",
        senha="123456"
    )
    db_session.add(other_user)
    db_session.commit()

    pedido = create_order(db_session, user)

    with pytest.raises(ForbiddenException):
        cancel_order(
            db=db_session,
            pedido_id=pedido.id,
            user=other_user
        )


# ----------------------------------------
# Finalizar pedido com sucesso
# Dono do pedido pode finalizar
# ----------------------------------------
def test_finalize_order_success(db_session, user):
    pedido = create_order(db_session, user)

    pedido_finalizado = finalize_order(
        db=db_session,
        pedido_id=pedido.id,
        user=user
    )

    assert pedido_finalizado.status == "FINALIZADO"


# ----------------------------------------
# Listar todos os pedidos (admin)
# Admin pode visualizar todos os pedidos
# ----------------------------------------
def test_list_all_orders_admin(db_session, admin):
    create_order(db_session, admin)

    pedidos = list_all_orders(
        db=db_session,
        user=admin
    )

    assert len(pedidos) == 1


# ----------------------------------------
# Listar todos os pedidos sem permissão
# Usuário comum não pode acessar
# ----------------------------------------
def test_list_all_orders_forbidden(db_session, user):
    with pytest.raises(ForbiddenException):
        list_all_orders(
            db=db_session,
            user=user
        )


# ----------------------------------------
# Listar pedidos do usuário autenticado
# Deve retornar apenas pedidos do próprio usuário
# ----------------------------------------
def test_list_user_orders(db_session, user):
    create_order(db_session, user)
    create_order(db_session, user)

    pedidos = list_user_orders(
        db=db_session,
        user=user
    )

    assert len(pedidos) == 2


# ----------------------------------------
# Buscar pedido por ID com sucesso
# Dono do pedido pode visualizar
# ----------------------------------------
def test_get_order_by_id_success(db_session, user):
    pedido = create_order(db_session, user)

    result = get_order_by_id(
        db=db_session,
        pedido_id=pedido.id,
        user=user
    )

    assert result.id == pedido.id


# ----------------------------------------
# Buscar pedido inexistente
# Deve lançar NotFoundException
# ----------------------------------------
def test_get_order_by_id_not_found(db_session, user):
    with pytest.raises(NotFoundException):
        get_order_by_id(
            db=db_session,
            pedido_id=999,
            user=user
        )


# ----------------------------------------
# Buscar pedido sem permissão
# Usuário que não é dono nem admin não pode acessar
# ----------------------------------------
def test_get_order_by_id_forbidden(db_session, user):
    other_user = Usuario(
        nome="Outro",
        email="outro2@test.com",
        senha="123456"
    )
    db_session.add(other_user)
    db_session.commit()

    pedido = create_order(db_session, user)

    with pytest.raises(ForbiddenException):
        get_order_by_id(
            db=db_session,
            pedido_id=pedido.id,
            user=other_user
        )


# ----------------------------------------
# Adicionar item ao pedido
# Deve recalcular o preço automaticamente
# ----------------------------------------
def test_add_item_to_order(db_session, user):
    pedido = create_order(db_session, user)

    item_data = OrderItem(
        quantidade=2,
        preco_unitario=30,
        sabor="CALABRESA",
        tamanho="MEDIA"
    )

    pedido_atualizado = add_item_to_order(
        db=db_session,
        pedido_id=pedido.id,
        item_data=item_data,
        user=user
    )

    assert len(pedido_atualizado.itens) == 1
    assert pedido_atualizado.preco == 60


# ----------------------------------------
# Remover item do pedido
# Deve recalcular o preço após remoção
# ----------------------------------------
def test_remove_item_from_order(db_session, user):
    pedido = create_order(db_session, user)

    item = ItemPedido(
        pedido=pedido.id,
        quantidade=1,
        preco_unitario=50,
        sabor="PORTUGUESA",
        tamanho="GRANDE"
    )
    db_session.add(item)
    db_session.commit()

    pedido_atualizado = remove_item_from_order(
        db=db_session,
        item_id=item.id,
        user=user
    )

    assert pedido_atualizado.preco == 0


# ----------------------------------------
# Remover item inexistente
# Deve lançar NotFoundException
# ----------------------------------------
def test_remove_item_not_found(db_session, user):
    with pytest.raises(NotFoundException):
        remove_item_from_order(
            db=db_session,
            item_id=999,
            user=user
        )
