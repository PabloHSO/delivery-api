# ----------------------------------------
# Testes de integração para as rotas de pedidos
# ----------------------------------------
from fastapi.testclient import TestClient
from app.main import app
from app.models.order import Pedido, ItemPedido


client = TestClient(app)

# ----------------------------------------
# Acessar rota base de pedidos
# Deve retornar mensagem e user_id
# ----------------------------------------
def test_orders_home(auth_headers):
    response = client.get(
        "/orders/",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert "message" in response.json()
    assert "user_id" in response.json()


# ----------------------------------------
# Criar pedido com sucesso
# Deve retornar 201 e o ID do pedido
# ----------------------------------------
def test_create_order_success(auth_headers):
    response = client.post(
        "/orders/pedido",
        headers=auth_headers
    )

    assert response.status_code == 201
    assert "pedido_id" in response.json()


# ----------------------------------------
# Cancelar pedido com sucesso
# Usuário dono pode cancelar
# ----------------------------------------
def test_cancel_order_success(auth_headers, db_session, user):
    pedido = Pedido(usuario=user.id)
    db_session.add(pedido)
    db_session.commit()

    response = client.post(
        f"/orders/pedido/cancelar/{pedido.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CANCELADO"


# ----------------------------------------
# Cancelar pedido inexistente
# Deve retornar 404
# ----------------------------------------
def test_cancel_order_not_found(auth_headers):
    response = client.post(
        "/orders/pedido/cancelar/999",
        headers=auth_headers
    )

    assert response.status_code == 404


# ----------------------------------------
# Listar pedidos do usuário autenticado
# Deve retornar lista de pedidos
# ----------------------------------------
def test_list_my_orders(auth_headers, db_session, user):
    pedido1 = Pedido(usuario=user.id)
    pedido2 = Pedido(usuario=user.id)
    db_session.add_all([pedido1, pedido2])
    db_session.commit()

    response = client.get(
        "/orders/meus_pedidos",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


# ----------------------------------------
# Visualizar pedido específico
# Deve retornar detalhes do pedido
# ----------------------------------------
def test_view_order_success(auth_headers, db_session, user):
    pedido = Pedido(usuario=user.id)
    db_session.add(pedido)
    db_session.commit()

    response = client.get(
        f"/orders/pedido/{pedido.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == pedido.id


# ----------------------------------------
# Visualizar pedido inexistente
# Deve retornar 404
# ----------------------------------------
def test_view_order_not_found(auth_headers):
    response = client.get(
        "/orders/pedido/999",
        headers=auth_headers
    )

    assert response.status_code == 404


# ----------------------------------------
# Adicionar item ao pedido
# Deve recalcular o preço corretamente
# ----------------------------------------
def test_add_item_to_order(auth_headers, db_session, user):
    pedido = Pedido(usuario=user.id)
    db_session.add(pedido)
    db_session.commit()
    db_session.refresh(pedido) 

    payload = {
        "quantidade": 2,
        "preco_unitario": 25,
        "sabor": "CALABRESA",
        "tamanho": "MEDIA"
        
    }

    response = client.post(
        f"/orders/pedido/adicionar_item/{pedido.id}",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["preco_total"] == 50


# ----------------------------------------
# Remover item do pedido
# Deve atualizar o preço após remoção
# ----------------------------------------
def test_remove_item_from_order(auth_headers, db_session, user):
    pedido = Pedido(usuario=user.id)
    db_session.add(pedido)
    db_session.commit()

    item = ItemPedido(
        pedido=pedido.id,
        quantidade=1,
        preco_unitario=40,
        sabor="PORTUGUESA",
        tamanho="GRANDE"
    )
    db_session.add(item)
    db_session.commit()

    response = client.delete(
        f"/orders/pedido/remover_item/{item.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["preco_total"] == 0


# ----------------------------------------
# Finalizar pedido
# Deve alterar status para FINALIZADO
# ----------------------------------------
def test_finalize_order_success(auth_headers, db_session, user):
    pedido = Pedido(usuario=user.id)
    db_session.add(pedido)
    db_session.commit()

    response = client.post(
        f"/orders/pedido/finalizar/{pedido.id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "FINALIZADO"
