from sqlalchemy.orm import Session
from app.models.user import Usuario
from app.schemas.user import UserCreate
from app.schemas.auth import UserLogin, TokenResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.core.exceptions import UnauthorizedException, ForbiddenException


# -------------------------------
# Cria novo usuário
# -------------------------------
def create_user(
    user_data: UserCreate,
    db: Session,
    current_user: Usuario
):
    """
    Cria um novo usuário no sistema.

    Regras:
    - Apenas administradores podem criar usuários admin
    - Email deve ser único
    """

    if user_data.admin and not current_user.admin:
        raise ForbiddenException(
            "Apenas administradores podem criar usuários administradores"
        )

    user_exists = (
        db.query(Usuario)
        .filter(Usuario.email == user_data.email)
        .first()
    )

    if user_exists:
        raise ForbiddenException("Email já cadastrado")

    hashed_password = hash_password(user_data.senha)

    user = Usuario(
        nome=user_data.nome,
        email=user_data.email,
        senha=hashed_password,
        ativo=user_data.ativo,
        admin=user_data.admin,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# -------------------------------
# Autentica usuário
# -------------------------------
def authenticate_user(
    login_data: UserLogin,
    db: Session
):
    """
    Autentica um usuário e gera token JWT.
    """

    user = (
        db.query(Usuario)
        .filter(Usuario.email == login_data.email)
        .first()
    )

    if not user or not verify_password(
        login_data.senha, user.senha
    ):
        raise UnauthorizedException("Credenciais inválidas")

    access_token = create_access_token(user_id=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# -------------------------------
# Renova token de acesso
# -------------------------------
def refresh_access_token(user: Usuario):
    """
    Gera um novo token de acesso para o usuário autenticado.
    """

    access_token = create_access_token(user_id=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
