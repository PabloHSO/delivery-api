from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    """
    Exceção para recursos não encontrados (404).
    Ex: pedido inexistente, usuário não encontrado, item inválido.
    """
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class UnauthorizedException(HTTPException):
    """
    Exceção para falhas de autenticação (401).
    Ex: token inválido, token expirado, usuário não autenticado.
    """
    def __init__(self, detail: str = "Não autenticado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(HTTPException):
    """
    Exceção para falhas de autorização (403).
    Ex: usuário sem permissão para acessar/modificar um recurso.
    """
    def __init__(self, detail: str = "Acesso não permitido"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class BadRequestException(HTTPException):
    """
    Exceção para requisições inválidas (400).
    Ex: dados inválidos, regra de negócio violada.
    """
    def __init__(self, detail: str = "Requisição inválida"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
