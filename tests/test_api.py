import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Banco em memória: os testes nunca tocam no finance.db real
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def nova_despesa(**extra):
    base = {
        "description": "Mercado",
        "amount": 150.5,
        "category": "alimentacao",
        "date": "2026-11-10",
    }
    return {**base, **extra}


def test_criar_despesa(client):
    resp = client.post("/expenses", json=nova_despesa())
    assert resp.status_code == 201
    assert resp.json()["id"] == 1
    assert resp.json()["category"] == "alimentacao"


def test_valor_invalido_retorna_422(client):
    resp = client.post("/expenses", json=nova_despesa(amount=0))
    assert resp.status_code == 422


def test_buscar_despesa_inexistente_retorna_404(client):
    assert client.get("/expenses/999").status_code == 404


def test_listar_e_deletar(client):
    client.post("/expenses", json=nova_despesa())
    assert len(client.get("/expenses").json()) == 1

    assert client.delete("/expenses/1").status_code == 204
    assert client.get("/expenses").json() == []


def test_resumo_mensal_agrupa_por_categoria(client):
    client.post("/expenses", json=nova_despesa(amount=100, category="alimentacao"))
    client.post("/expenses", json=nova_despesa(amount=50, category="alimentacao"))
    client.post("/expenses", json=nova_despesa(amount=30, category="transporte"))
    client.post("/expenses", json=nova_despesa(amount=999, date="2026-10-05"))

    resp = client.get("/summary/2026/11")
    assert resp.status_code == 200
    assert resp.json()["total"] == 180
    assert resp.json()["by_category"] == {"alimentacao": 150, "transporte": 30}