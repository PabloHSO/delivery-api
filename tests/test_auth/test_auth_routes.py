import pytest

# ----------------------------------------
# Cadastro de usuário
# ----------------------------------------
def test_signup_success(client, auth_headers):
    # Teste real de signup
    response = client.post(
        "/auth/sign-up",
        json={
            "nome": "João",
            "email": "joao@test.com",
            "senha": "123456",
            "ativo": True,
            "admin": False
        },
        headers=auth_headers  # Usar token para criar usuário
    )

    # Deve retornar 201 se signup funcionar
    assert response.status_code == 201, f"Signup falhou: {response.text}"
    assert response.json()["message"] == "Usuário criado com sucesso"


# ----------------------------------------
# Login com sucesso (JWT)
# ----------------------------------------
def test_login_success(client, user):
    # Login do usuário criado pela fixture 'user'
    response = client.post(
        "/auth/sign-in-form",  # endpoint OAuth2 correto
        data={
            "username": user.email,
            "password": "123456"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200, f"Login falhou: {response.text}"
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


# ----------------------------------------
# Login com senha inválida
# ----------------------------------------
def test_login_invalid_password(client, user):
    response = client.post(
        "/auth/sign-in-form",
        data={
            "username": user.email,
            "password": "123456WRONG"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401, f"Senha inválida deveria retornar 401: {response.text}"


# ----------------------------------------
# Acesso a rota protegida sem token
# ----------------------------------------
def test_protected_route_without_token(client):
    response = client.get("/orders")
    assert response.status_code == 401, f"Rota protegida sem token deveria retornar 401"


# ----------------------------------------
# Acesso a rota protegida com token válido
# ----------------------------------------
def test_protected_route_with_token(client, auth_headers):
    response = client.get(
        "/orders",
        headers=auth_headers  # token válido vindo da fixture
    )

    assert response.status_code == 200, f"Rota protegida com token válido falhou: {response.text}"
