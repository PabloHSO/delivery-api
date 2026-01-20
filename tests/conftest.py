import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_session
from app.models.base import Base
from app.models.user import Usuario
from app.models.order import Pedido, ItemPedido
from app.core.security import hash_password

# Banco de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./banco.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------
# Fixture de banco de dados
# ---------------------------
@pytest.fixture
def db_session():
    # Cria todas as tabelas antes do teste
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# ---------------------------
# Fixture de TestClient
# ---------------------------
@pytest.fixture
def client(db_session):
    # Override do get_session
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

# ---------------------------
# Usuário comum
# ---------------------------
@pytest.fixture
def user(db_session):
    user = Usuario(
        nome="User",
        email="user@test.com",
        senha=hash_password("123456"),
        ativo=True,
        admin=False
    )
    db_session.add(user)
    db_session.commit()
    return user

# ---------------------------
# Usuário admin
# ---------------------------
@pytest.fixture
def admin(db_session):
    admin = Usuario(
        nome="Admin",
        email="admin@test.com",
        senha=hash_password("123456"),
        ativo=True,
        admin=True
    )
    db_session.add(admin)
    db_session.commit()
    return admin

# ---------------------------
# Headers auth usuário comum
# ---------------------------
@pytest.fixture
def auth_headers(client, user):
    response = client.post(
        "/auth/sign-in-form",
        data={"username": user.email, "password": "123456"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, f"Login falhou: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# ---------------------------
# Headers auth admin
# ---------------------------
@pytest.fixture
def auth_headers_admin(client, admin):
    response = client.post(
        "/auth/sign-in-form",
        data={"username": admin.email, "password": "123456"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, f"Login admin falhou: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
