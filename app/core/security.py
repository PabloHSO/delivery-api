from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign_in_form")

def hash_password(password: str) -> str:
    """
    Gera hash bcrypt seguro para a senha.
    Retorna string UTF-8 compatível.
    """
    # bcrypt.hashpw sempre recebe bytes
    salt = bcrypt.gensalt()  # gera salt seguro aleatório
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")  # armazena como string no DB


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica se a senha fornecida bate com o hash armazenado.
    """
    # Converte hash armazenado de volta para bytes
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
