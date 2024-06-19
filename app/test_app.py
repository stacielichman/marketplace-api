import pytest
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


# def test_create_product():
#     product_data = {
#         "title": "test_product",
#         "description": "test_description",
#         "count": 100,
#         "price": 99.99,
#         "user_id": 1
#     }
#
#     response =client.post('/products/', data=product_data)
#     assert response.status_code == 200


def test_get_product() -> None:
    response = client.get("products")
    assert response.status_code == 200
