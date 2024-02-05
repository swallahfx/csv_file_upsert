# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from product_app.main import app
from product_app.schema import ProductSchema


app.dependency_overrides[ProductSchema.validate_objects] = MagicMock(return_value=[{}])

@pytest.fixture
def mock_app():
    return TestClient(app)


def test_upload_csv(mock_app: TestClient):
    with patch("product_app.main.process_csv", return_value=[]):
        response = mock_app.post("/upload_products/", data={"file": "fake.csv"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Product Creation/Upload Successful"}


def test_list_products(mock_app: TestClient):
    with patch("product_app.main.get_all_products", return_value=[]):
        response = mock_app.get("/get_products/")
    
    assert response.status_code == 200
    assert response.json() == {'products': []}


def test_upload_csv_internal_error(mock_app: TestClient):
    with patch("product_app.main.process_csv", side_effect=Exception("Some error")):
        response = mock_app.post("/upload_products/", data={"file": "fake.csv"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Error: Some error"}

