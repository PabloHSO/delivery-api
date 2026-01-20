from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.user import Usuario
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse, UserLogin
from app.core.deps import get_current_user
from app.services.auth_service import (
    create_user,
    authenticate_user,
    refresh_access_token,
)
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# -------------------------------------------------
# Rota base de autenticação
# -------------------------------------------------
@auth_router.get("/")
def auth_home():
    """
    Rota base do módulo de autenticação.

    Usada como health check e documentação.
    """
    return {
        "message": "Você acessou o módulo de autenticação",
        "authenticated": False
    }



# -------------------------------------------------
# Cadastro de usuário
# -------------------------------------------------
@auth_router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED
)
def sign_up(
    user_data: UserCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria um novo usuário no sistema.

    Apenas administradores podem criar usuários admin.
    """
    user = create_user(
        user_data=user_data,
        db=db,
        current_user=current_user
    )

    return {
        "message": "Usuário criado com sucesso",
        "user_id": user.id,
        "email": user.email
    }



# -------------------------------------------------
# Login via JSON (frontend / API)
# -------------------------------------------------
@auth_router.post(
    "/sign-in",
    response_model=TokenResponse
)
def sign_in(
    login_data: UserLogin,
    db: Session = Depends(get_session)
):
    """
    Autentica o usuário e retorna um token JWT.
    """
    return authenticate_user(
        login_data=login_data,
        db=db
    )


# -------------------------------------------------
# Login OAuth2 (Swagger / OpenAPI)
# -------------------------------------------------
@auth_router.post(
    "/sign-in-form",
    response_model=TokenResponse
)
def sign_in_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    """
    Autenticação via formulário (OAuth2).

    Usado pelo Swagger UI.
    """
    login_data = UserLogin(
        email=form_data.username,
        senha=form_data.password
    )

    return authenticate_user(
        login_data=login_data,
        db=db
    )


# -------------------------------------------------
# Renovação do token de acesso
# -------------------------------------------------
@auth_router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_token(
    user: Usuario = Depends(get_current_user)
):
    """
    Gera um novo token de acesso usando o token atual.
    """
    return refresh_access_token(user)
