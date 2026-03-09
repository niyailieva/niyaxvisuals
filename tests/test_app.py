import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_portfolio_page_loads(client):
    response = client.get("/portfolio")
    assert response.status_code == 200


def test_admin_requires_login(client):
    response = client.get("/admin/portfolio/new")
    assert response.status_code in (302, 401, 403)