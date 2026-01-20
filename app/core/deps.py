from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.core.security import oauth2_scheme
from app.core.config import settings
from app.models.user import Usuario
from app.core.exceptions import UnauthorizedException

def get_current_user(
    db: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
    except JWTError:
        raise UnauthorizedException()

    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if not user:
        raise UnauthorizedException()

    return user