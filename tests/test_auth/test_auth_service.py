from app.schemas.auth import UserLogin
from app.schemas.user import UserCreate
import pytest
from app.services.auth_service import (
    create_user,
    authenticate_user
)
from app.models.user import Usuario
from app.core.exceptions import UnauthorizedException

# ----------------------------------------
# Testes unitários para o serviço de autenticação
# ----------------------------------------

# ----------------------------------------
# Criar usuário com sucesso
# ----------------------------------------

# -------------------------------
# Teste de criação de usuário
# -------------------------------
def test_create_user_success(db_session, admin):
    user_data = UserCreate(
        nome="User",
        email="user@test.com",
        senha="123456",
        admin=False,
        ativo=True
    )

    user = create_user(
        user_data=user_data,
        db=db_session,
        current_user=admin
    )

    assert user.email == "user@test.com"
    assert user.nome == "User"
    assert user.admin is False
    assert user.ativo is True


# -------------------------------
# Teste de autenticação com sucesso
# -------------------------------
def test_authenticate_user_success(db_session, admin):
    # Primeiro cria usuário
    user_data = UserCreate(
        nome="Maria",
        email="maria@test.com",
        senha="123456",
        admin=False,
        ativo=True
    )
    create_user(user_data=user_data, db=db_session, current_user=admin)

    login_data = UserLogin(
        email="maria@test.com",
        senha="123456"
    )

    token = authenticate_user(login_data=login_data, db=db_session)

    assert "access_token" in token
    assert token["token_type"] == "bearer"


# -------------------------------
# Teste de senha inválida
# -------------------------------
def test_authenticate_user_invalid_password(db_session, admin):
    user_data = UserCreate(
        nome="Carlos",
        email="carlos@test.com",
        senha="123456",
        admin=False,
        ativo=True
    )
    create_user(user_data=user_data, db=db_session, current_user=admin)

    login_data = UserLogin(
        email="carlos@test.com",
        senha="senha_errada"
    )

    with pytest.raises(Exception):
        authenticate_user(login_data=login_data, db=db_session)


# -------------------------------
# Teste de usuário não encontrado
# -------------------------------
def test_authenticate_user_not_found(db_session):
    login_data = UserLogin(
        email="inexistente@test.com",
        senha="123456"
    )

    with pytest.raises(Exception):
        authenticate_user(login_data=login_data, db=db_session)
